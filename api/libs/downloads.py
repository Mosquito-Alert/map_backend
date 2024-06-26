"""Userfixes Libraries."""
from http import HTTPStatus
from django.db.models.functions import Concat
from datetime import datetime, timezone, timedelta
from .base import BaseManager
from api.models import MapAuxReport
from django.conf import settings
import tempfile
import os
import json
import json
import zipfile
import geopandas
from django.http import HttpResponse, JsonResponse
from shapely.geometry import Point
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import CharField, Value
from django.db.models import Q
import operator 
from functools import reduce
from django.core.serializers import serialize
import numpy as np
from api.constants import (site_value, public_download_fields,
                           private_download_fields, private_fields, public_fields)

def getValueOrNull(key, values):
    key = str(key)
    if key in values:
        return values[key]
    else:
        return 'unkown'

def getFormatedResponses(type, responses, private_webmap_layer):
    locations = {
        '44': 'Unknown', '43': 'Outdoors',
        '42': 'Inside building','41': 'Inside vehicle'
    }
    biteTimes = {
        '31': 'At sunrise', '32': 'At noon',
        '33': 'At sunset', '34': 'At night',
        '35': 'Not really sure'
    }
    bodyParts = {
        '21': 'Head', '22': 'Left arm',
        '23': 'Right arm', '24': 'Chest',
        '25': 'Left leg', '26': 'Right leg'
    }
    waterStatus = {
        '101': 'Yes',
        '81': 'No'
    }
    withLarva = { '81': 'No', '101': 'Yes' }

    NUMBER_OF_BITES = 1
    WHERE_DID_THEY_BITE_YOU = 4
    BITE_TIME = 3
    BODY_PART_BITTEN = 2
    SITE_WATER_STATUS = 10
    SITE_LARVA_STATUS = 17
    formated = {}

    if type.lower() == 'bite':
        for response in responses:
            if not response ['question_id'] is None:
                if response['question_id'] == NUMBER_OF_BITES:
                    formated['howManyBites'] = response['answer_value']

                elif response['question_id'] == WHERE_DID_THEY_BITE_YOU:
                    formated['location'] = getValueOrNull(response['answer_id'], locations)

                elif response['question_id'] == BITE_TIME:
                    formated['biteTime'] = getValueOrNull(response['answer_id'], biteTimes)

                elif response['question_id'] == BODY_PART_BITTEN:
                    formated['bodyPart'] = getValueOrNull(response['answer_id'], bodyParts)

    else:
        EXISTS_WATER_STATUS = False
        EXISTS_LARVA_STATUS = False
        for response in responses:
            if not response ['question_id'] is None:
                if response['question_id'] == SITE_WATER_STATUS:
                    EXISTS_WATER_STATUS = True
                    formated['with_water'] = getValueOrNull(response['answer_id'], waterStatus)

                if response['question_id'] == SITE_LARVA_STATUS:
                    EXISTS_LARVA_STATUS = True
                    formated['with_larva'] = getValueOrNull(response['answer_id'], withLarva)
            # If info not found, then take data from other attributes
        if not EXISTS_WATER_STATUS:
            if private_webmap_layer.lower() == 'storm_drain_water':
                formated['with_water'] = getValueOrNull('101', waterStatus)
            elif private_webmap_layer.lower() == 'storm_drain_dry':
                formated['with_water'] = getValueOrNull('81', waterStatus)
            else:
                formated['with_water'] = 'Not available'
        if not EXISTS_WATER_STATUS:
            formated['with_larva'] = 'Not available'
    return formated


class DownloadsManager(BaseManager):
    """Main Observations Downloads Library."""

    def __init__(self, request):
        """Constructor."""

        self.request = request


    def _get_main_data(self):
        """Return the data without filtering."""

        if self.request.user.is_authenticated:
            fields = public_download_fields + private_download_fields
        else:
            fields = public_download_fields

        qs = MapAuxReport.objects.filter(
                lat__isnull = False
            ).filter(
                lon__isnull = False
            ).filter(
                private_webmap_layer__isnull = False
            ).annotate(
                map_link=Concat(Value(settings.WEBSERVER_URL), 'version_uuid')
            ).values(*fields)
        return qs

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
            if dates['from'] != '':
                if dates['from'] is not None and dates['to'] is not None:
                    self.data = self.data.filter(
                    observation_date__gte=datetime.strptime(dates['from'], "%Y-%m-%d").replace(tzinfo=timezone.utc),
                    observation_date__lt=(datetime.strptime(dates['to'], "%Y-%m-%d").replace(tzinfo=timezone.utc) +
                                timedelta(days=1))
                )

        # There can be only one report
        if 'report_id' in filters:
            reports = filters['report_id']
            self.data = self.data.filter(report_id__in=reports)


        # Check if there is a location to filter for
        if 'location' in filters:
                # location = json.loads(filters['location'])
                location = filters['location']
                # BB = json.loads(filters['locationBbox'])
                condition = """
                    ST_CONTAINS(
                        ST_SETSRID(ST_GEOMFROMGEOJSON('{}'),4326),
                        ST_SETSRID(ST_MAKEPOINT(LON,LAT), 4326)
                    )
                """.format(location)
                self.data = self.data.extra(where=[condition])

        if layers is not None:
            self.data = self.data.filter(
                private_webmap_layer__in=layers
            )


        if 'hashtags' in filters:
            hashtags = json.loads(filters['hashtags'])
            q_collect = None
            rules = []
            for tag in hashtags:
                formatHashtag =  tag + ' ' if tag.startswith('#') else ('#' + tag)
                hashtagWord = tag + ' '
                rules.append(Q(note__icontains=hashtagWord))
                rules.append(Q(note__iendswith=formatHashtag))

            self.data = self.data.filter(reduce(operator.or_, rules))

        return self.data

    def get(self, filters, fext):
        """Return Observations as attachment zip file."""

        # Main query
        self.data = self._get_main_data()

        # Filter data
        try:
            qs = self._filter_data(**filters)
        except Exception as e:
            return JsonResponse({ "status": "error", "msg": str(e) }, status = HTTPStatus.BAD_REQUEST)

        file_name = 'observations'

        with tempfile.TemporaryDirectory() as tmp_dir:
            df = geopandas.GeoDataFrame(list(self.data))

            if qs.count() != 0:
                df["observation_date"] = df["observation_date"].astype(str)

            df['larvae'] = np.where(
                        (df['type'] == site_value),
                        df["larvae"].map({True: 'YES', False: 'NO', None: 'NA'}),      #We place column3 values
                        df['larvae'])

            df['larvae'] = np.where(
                        (df['type'] != site_value),
                        None,      #We place column3 values
                        df['larvae'])

            # df["larvae"] = df["larvae"].map({True: 'YES', False: 'NO', None: 'NA'})
            df.rename(columns = {
                    'version_uuid':'id',
                    'report_id': 'code',
                    'observation_date':'date',
                    'lon':'longitude',
                    'lat':'latitude',
                    'ref_system': 'ref_system',
                    'nuts0_code': 'nuts0_id',
                    'nuts0_name': 'nuts0_name',
                    'nuts3_code': 'nuts3_id',
                    'nuts3_name': 'nuts3_name',
                    'lau_code': 'lau_id',
                    'lau_name': 'lau_name',
                    'type':'type',
                    'expert_validated':'validation',
                    'private_webmap_layer':'category',
                    'ia_value': 'ai value',
                    'larvae': 'larvae',
                    'bite_count': 'bite_count',
                    'bite_location': 'bite_location',
                    'bite_time': 'bite_time',
                    'note': 'tags (PRIVATE!!!)',
                    'map_link': 'map_link'
                }, inplace = True)


            if fext.lower() == 'gpkg':
                geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
                gdf = geopandas.GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
                gdf.to_file(os.path.join(tmp_dir, f'{file_name}.gpkg'), driver='GPKG')
            else:
                df.to_excel(os.path.join(tmp_dir, f'{file_name}.xlsx'),  index = False)

            # Zip the exported files to a single file
            tmp_zip_file_name = f'{file_name}.zip'
            tmp_zip_file_path = f"{tmp_dir}/{tmp_zip_file_name}"
            tmp_zip_obj = zipfile.ZipFile(tmp_zip_file_path, 'w')

            for file in os.listdir(tmp_dir):
                if file != tmp_zip_file_name:
                    tmp_zip_obj.write(os.path.join(tmp_dir, file), file)

            # Add metadata files
            if self.request.user.is_authenticated:
                folder = settings.DOWNLOAD_REGISTERED_METADATA_FILES_LOCATION
            else:
                folder = settings.DOWNLOAD_PUBLIC_METADATA_FILES_LOCATION

            for file in os.listdir(folder):
                tmp_zip_obj.write(os.path.join(folder, file), file)

            tmp_zip_obj.close()

            # Return the file
            with open(tmp_zip_file_path, 'rb') as file:
                response = HttpResponse(file, content_type='application/force-download')
                response['Content-Disposition'] = f'attachment; filename="{tmp_zip_file_name}"'
                response['status'] = HTTPStatus.OK
                return response

    def getGeoJson(self, filters):
        """Return GeoJson Observations as json."""
        # Main query
        self.data = self._get_main_data()

        # Filter data
        try:
            qs = self._filter_data(**filters)
        except Exception as e:
            return JsonResponse({ "status": "error", "msg": str(e) }, status = HTTPStatus.BAD_REQUEST)

        result = []
        if self.request.user.is_authenticated:
            fields = private_fields + public_fields
        else:
            fields = public_fields

        for r in qs.values(*fields):
            if (r['type'].lower() in ['bite', 'site']):
                r['formatedResponses'] = getFormatedResponses(
                                            r['type'],
                                            json.loads(r['responses_json']),
                                            r['private_webmap_layer']
                                        )
            result.append(r)

        return JsonResponse(result, safe=False, status = HTTPStatus.OK)

