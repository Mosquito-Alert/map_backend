import random
from re import M
from django.shortcuts import render
from django.templatetags.static import static
from django.http import JsonResponse, HttpResponse
from .models import MapAuxReport
from django.core.serializers import serialize
import json
from django.db import connection
    
def get_feature(request, observation_id):
    """Return a feature."""
    # Mock up some random data
    data = {
        'layer': 'mosquito_tiger_confirmed',
        'date': '21-02-2021',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vitae magna nulla. Integer vitae tempor felis. Phasellus ornare risus non lacus sagittis, eget pulvinar metus consectetur. Ut non viverra libero. Maecenas laoreet sapien quis imperdiet iaculis. Morbi vulputate porta odio, a tincidunt lacus sagittis et. Nam hendrerit erat est, ac tincidunt nisl ultrices non.'
    }
    if random.random() > 0.5:
        data["layer"] = 'mosquito_tiger_probable'
    if random.random() > 0.5:
        data["description"] = 'Lorem ipsum dolor sit amet.'
    if random.random() > 0.5:
        data["photo_url"] = 'http://localhost:8000/static/api/mosquito/dummy.jpg'
    return JsonResponse(data)

def get_report(request, report_id):
    SQL = f"""
        SELECT jsonb_build_object(
            'type',     'FeatureCollection',
            'features', jsonb_agg(features.feature)
		)   FROM(
			SELECT row_to_json(f) As feature
				 FROM (
			 SELECT 'Feature' As type
				  , ST_AsGeoJSON(st_setsrid(st_makepoint(lon, lat), 4326),6)::json As geometry
				  ,row_to_json((SELECT l FROM (
					  SELECT id, observation_date::date as d, private_webmap_layer as c,
					  -- tags is string with square braquets, so firt remove them and cast to array
					  coalesce(
						  replace(regexp_replace(tags, '\[|\]', '', 'g'), '''', ''),
					      '') as t
					) As l
				  )) As properties
				   FROM map_aux_reports
				   WHERE lat is not null and lon is not null AND report_id = '{report_id}'
				   ORDER BY observation_date
			) As f
		) as features
        """
    with connection.cursor() as cursor:
        cursor.execute(SQL)
        data = cursor.fetchall()[0]
        # data = serialize("json", cursor.fetchone())

    return HttpResponse(data, content_type="application/json")

def get_observation(request, observation_id):
    qs = MapAuxReport.objects.get(pk = observation_id)
    data = serialize("json", [qs])
    r = json.loads(data)[0]['fields']
    r['responses_json'] = json.loads(r['responses_json'])
    if (r['type'].lower() in ['bite', 'site']):
        r['formatedResponses'] = getFormatedResponses(r['type'], r['responses_json'], r['private_webmap_layer'])
    return HttpResponse(json.dumps(r), content_type="application/json")

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
        '101': 'Breeding site with water',
        '81': 'Breeding site without water'
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


    def userfixes(request, startdate, enddate):
        return 