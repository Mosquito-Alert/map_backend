from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
import random
from re import M
from django.shortcuts import render
from django.templatetags.static import static
from django.http import JsonResponse, HttpResponse
from .models import MapAuxReport
from django.core.serializers import serialize
import json
from django.db import connection
from .libs.userfixes import UserfixesManager
from .libs.downloads import DownloadsManager
from .libs.shareview import ShareViewManager
from .libs.reportview import ReportManager

@csrf_exempt
def downloads(request, fext):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        manager = DownloadsManager(request)
        if (fext == 'features'):
            return manager.getGeoJson(post_data)
        else:
            return manager.get(post_data, fext)            

# Share Map View
@csrf_exempt
def saveView(request):
    if request.method == "POST":
        manager = ShareViewManager()
        return manager.save(request)

@csrf_exempt
def loadView(request, code):
    if request.method == "GET":
        manager = ShareViewManager()
        return manager.load(code)

# Map Report
@csrf_exempt
def saveReport(request):
    if request.method == "POST":
        manager = ReportManager()
        return manager.save(request)

@csrf_exempt
def loadReport(request, code):
    if request.method == "GET":
        manager = ReportManager()
        return manager.load(code)


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

# @cache_page(86400)
def get_data(request, year):
    SQL = f"""
        SELECT jsonb_build_object(
            'year', {year},            
            'type',     'FeatureCollection',
            'features', jsonb_agg(features.feature)
        )
        from(
            -- one raw for each feature
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
                    WHERE extract(year from observation_date) = {year} 
                        AND LAT IS NOT NULL
                        AND LON IS NOT NULL
                        AND PRIVATE_WEBMAP_LAYER IN ('mosquito_tiger_probable',
                            'mosquito_tiger_confirmed', 'yellow_fever_probable', 'yellow_fever_confirmed',
                            'japonicus_probable', 'japonicus_confirmed', 'japonicus_koreicus',
                            'koreicus_probable', 'koreicus_confirmed', 'japonicus_koreicus',
                            'culex_probable', 'culex_confirmed','unidentified', 'other_species','bite',
                            'storm_drain_water','storm_drain_dry','breeding_site_other')
                    ORDER BY observation_date
            ) As f
        ) as features
    """

    try:
        cursor = connection.cursor()
        cursor.execute(SQL)
        data = cursor.fetchall()[0]

        # if year == '2019':
        #     raise Exception('Error fetching data (%s)' % year)

    except Exception as e:
        return JsonResponse({ "status": "error", "msg": str(e) })
    else:
        return HttpResponse(data, content_type="application/json")



@csrf_exempt
def get_reports(request):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        reports = post_data['reports'].split(',')
        reports_str = ','.join("'" + r  + "'" for r in reports)
        
    else: 
        return HttpResponse({}, content_type="application/json")

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
					  SELECT id, observation_date::date as d, private_webmap_layer as c, report_id,
					  -- tags is string with square braquets, so firt remove them and cast to array
					  coalesce(
						  replace(regexp_replace(tags, '\[|\]', '', 'g'), '''', ''),
					      '') as t
					) As l
				  )) As properties
				   FROM map_aux_reports
				   WHERE lat is not null and lon is not null AND report_id in ({reports_str})
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

def get_observation_by_id(request, id):
    qs = MapAuxReport.objects.get(version_uuid = id)
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


# def userfixes(request, startdate, enddate):
#     return True

# @cache_page(36000)
def userfixes(request, **filters):
    """Get Coverage Layer Info."""
    manager = UserfixesManager(request)
    return manager.get('GeoJSON', **filters)    