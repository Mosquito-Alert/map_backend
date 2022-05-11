"""Userfixes Libraries."""
from datetime import datetime, timedelta
from operator import __or__ as OR
from .base import BaseManager
from api.models import MapAuxReport
from django.conf import settings
import tempfile
import os
import zipfile
import geopandas
from django.http import HttpResponse
from shapely.geometry import Point

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
        dates = filters['date'][0]
        # hashtags = filters['hashtags']
        # ids = filters['ids']
        
        # if hashtags is not None:
        #     self.data = self.data.filter(
        #         tags__iregex=r'(' + '|'.join(hashtags) + ')'
        #     ) 

        if bbox is not None:
            self.data = self.data.filter(
                lon__gte=bbox[0],
                lon__lt=bbox[2],
                lat__gte=bbox[1],
                lat__lt=bbox[3]
            )

        if layers is not None:
            self.data = self.data.filter(
                private_webmap_layer__in=layers
            )            

        if dates['from'] is not None and dates['to'] is not None:
            self.data = self.data.filter(
                observation_date__gte=datetime.strptime(dates['from'], "%Y/%m/%d"),
                observation_date__lt=(datetime.strptime(dates['to'], "%Y/%m/%d") +
                              timedelta(days=1))
            )
        
        return self.data

    def get(self, filters):
        """Return Observations."""
        print('filter data')

        # Main query
        self.data = self._get_main_data()

        # Filter data
        qs = self._filter_data(**filters)
        file_name = 'observations'
        df = geopandas.GeoDataFrame(list(qs.values()))
        df["observation_date"] = df["observation_date"].astype(str)

        geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
        gdf = geopandas.GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)

        with tempfile.TemporaryDirectory() as tmp_dir:
            print(tmp_dir)
            # Export gdf as shapefile
            gdf.to_file(os.path.join(tmp_dir, f'{file_name}.shp'), driver='ESRI Shapefile')
            # gdf.to_file(os.path.join(tmp_dir, f'{file_name}.gpkg'), driver='GPKG')


            # Zip the exported files to a single file
            tmp_zip_file_name = f'{file_name}.zip'
            tmp_zip_file_path = f"{tmp_dir}/{tmp_zip_file_name}"
            
            tmp_zip_obj = zipfile.ZipFile(tmp_zip_file_path, 'w')

            for file in os.listdir(tmp_dir):
                if file != tmp_zip_file_name:
                    tmp_zip_obj.write(os.path.join(tmp_dir, file), file)

            tmp_zip_obj.close()

            # Return the file
            with open(tmp_zip_file_path, 'rb') as file:
                response = HttpResponse(file, content_type='application/force-download')
                response['Content-Disposition'] = f'attachment; filename="{tmp_zip_file_name}"'
                return response