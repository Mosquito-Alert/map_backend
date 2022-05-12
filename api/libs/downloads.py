"""Userfixes Libraries."""
from datetime import datetime, timedelta
from operator import __or__ as OR
from .base import BaseManager
from api.models import MapAuxReport
from django.conf import settings
import tempfile
import os
import json
import zipfile
import geopandas
from django.http import HttpResponse
from shapely.geometry import Point
from django.apps import apps


class DownloadsManager(BaseManager):
    """Main Observations Downloads Library."""
    
    def _get_main_data(self):
        """Return the data without filtering."""
        return MapAuxReport.objects.all().filter(
                lat__isnull = False
            ).filter(
                lon__isnull = False
            ).filter(
                private_webmap_layer__isnull = False
            )

    def _filter_data(self, **filters):
        """Return data filtered according to time parameters."""
        bbox = filters['bbox']
        layers = filters['observations']
        
        if bbox is not None:
            self.data = self.data.filter(
                lon__gte=bbox[0],
                lon__lt=bbox[2],
                lat__gte=bbox[1],
                lat__lt=bbox[3]
            )

        # Check if there is date to filter for
        if 'date' in filters:
            dates = filters['date'][0]
            if dates['from'] is not None and dates['to'] is not None:
                self.data = self.data.filter(
                observation_date__gte=datetime.strptime(dates['from'], "%Y/%m/%d"),
                observation_date__lt=(datetime.strptime(dates['to'], "%Y/%m/%d") +
                              timedelta(days=1))
            )

        # There can be only one report
        if 'report_id' in filters:
            reports = filters['report_id']
            for report in reports:
                self.data = self.data.filter(report_id__icontains=report)

        # Check if there is a location to filter for
        if 'location' in filters:
                # location = json.loads(filters['location'])
                location = filters['location']
                condition = """
                    ST_CONTAINS(
                        ST_GEOMFROMGEOJSON('{}'),
                        ST_SETSRID(ST_MAKEPOINT(LON,LAT), 4326)
                    )
                """.format(location)
                self.data = self.data.extra(where=[condition])

        if layers is not None:
            self.data = self.data.filter(
                private_webmap_layer__in=layers
            )            


        if 'hashtags' in filters:
            tags = json.loads(filters['hashtags'])
            # tags_str = "'{0}'".format("', '".join(tags))
            for tag in tags:
                self.data = self.data.filter(tags__icontains=tag)

        return self.data

    def get(self, filters):
        """Return Observations."""

        # Main query
        self.data = self._get_main_data()

        # Filter data
        qs = self._filter_data(**filters)
        if qs.count() == 0:
            return {}

        file_name = 'observations'
        df = geopandas.GeoDataFrame(list(qs.values()))
        df["observation_date"] = df["observation_date"].astype(str)

        geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
        gdf = geopandas.GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Export gdf as shapefile
            # gdf.to_file(os.path.join(tmp_dir, f'{file_name}.shp'), driver='ESRI Shapefile')
            gdf.to_file(os.path.join(tmp_dir, f'{file_name}.gpkg'), driver='GPKG')


            # Zip the exported files to a single file
            tmp_zip_file_name = f'{file_name}.zip'
            tmp_zip_file_path = f"{tmp_dir}/{tmp_zip_file_name}"
            
            tmp_zip_obj = zipfile.ZipFile(tmp_zip_file_path, 'w')

            for file in os.listdir(tmp_dir):
                if file != tmp_zip_file_name:
                    tmp_zip_obj.write(os.path.join(tmp_dir, file), file)

            # Add datada files
            folder = settings.DOWNLOAD_METADATA_FILES_LOCATION
            
            for file in os.listdir(folder):
                tmp_zip_obj.write(os.path.join(folder, file), file)

            tmp_zip_obj.close()

            # Return the file
            with open(tmp_zip_file_path, 'rb') as file:
                response = HttpResponse(file, content_type='application/force-download')
                response['Content-Disposition'] = f'attachment; filename="{tmp_zip_file_name}"'
                return response