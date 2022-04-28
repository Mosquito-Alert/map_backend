"""Userfixes Libraries."""
from datetime import datetime, timedelta
from operator import __or__ as OR
from functools import reduce
from django.db.models import Count, Q

from .base import BaseManager
from api.constants import gridsize
from api.models import Userfixes


class UserfixesManager(BaseManager):
    """Main Userfixes Library."""

    def _userfixes_get_gridsize(self):
        """Return the size of the grid."""
        # Return a constant. Calculating the grid size increases the time.
        return gridsize

    def _get_main_data(self):
        """Return the data without filtering."""
        return Userfixes.objects.all().values(
            'masked_lon', 'masked_lat'
        ).order_by('masked_lat', 'masked_lon').annotate(
            n_fixes=Count('pk', distinct=True)
        )

    def _filter_data(self, **filters):
        """Return data filtered according to time parameters."""
        startdate = filters['startdate']
        enddate = filters['enddate']
        if startdate is not None and enddate is not None:
            self.data = self.data.filter(
                fix_time__gte=datetime.strptime(startdate, "%Y-%m-%d"),
                fix_time__lt=(datetime.strptime(enddate, "%Y-%m-%d") +
                              timedelta(days=1))
            )

    def _as_geojson(self):
        """Return the GeoJSON representation of the userfixes."""
        # Main object
        geojson = {
            "type": 'FeatureCollection',
            "features": []
        }
        # Iterate through fixes
        for fix in (self.data.values(
                        'masked_lon', 'masked_lat', 'n_fixes'
                    ).iterator()):
            min_lon = round(fix['masked_lon'], 3)
            min_lat = round(fix['masked_lat'], 3)
            max_lon = round(fix['masked_lon'] + self.gridsize, 3)
            max_lat = round(fix['masked_lat'] + self.gridsize, 3)
            geojson['features'].append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [[
                        [min_lon, min_lat], [min_lon, max_lat],
                        [max_lon, max_lat], [max_lon, min_lat],
                        [min_lon, min_lat]
                    ]]
                },
                'properties': {'num_fixes': fix['n_fixes']}
            })
        # Return
        return geojson

    def get(self, format='GeoJSON', **filters):
        """Return the userfixes."""
        # Main query
        self.data = self._get_main_data()
        # Get grid size
        # This needs to be done before filtering, otherwise we might not have
        # enough data to detect the grid size
        self.gridsize = self._userfixes_get_gridsize()
        # Filter data
        self._filter_data(**filters)
        # Build the GeoJSON
        if format.lower() == 'geojson':
            self.response = self._as_geojson()
        # Return
        return self._end()
