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
import os
from django.conf import settings
from .utils import get_directory_structure
from api.constants import (
    VECTORS_MODEL_NAMES, VECTORS_MODEL_FOLDER,
    VECTORS_FILE_NAME, VECTORS_FILE_EXTENSION,
    BITES_MODEL_FOLDER, BITES_FILE_NAME, BITES_FILE_EXTENSION
)
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache, cache_page

ACC_HEADERS = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
               'Access-Control-Max-Age': 1000,
               'Access-Control-Allow-Headers': '*'}

def cross_domain_ajax(func):
    """Set Access Control request headers."""
    def wrap(request, *args, **kwargs):
        # Firefox sends 'OPTIONS' request for cross-domain javascript call.
        if request.method != "OPTIONS":
            response = func(request, *args, **kwargs)
        else:
            response = HttpResponse()
        for k, v in ACC_HEADERS.items():
            response[k] = v
        return response
    return wrap

@csrf_exempt
@never_cache
@cross_domain_ajax
@csrf_exempt
@never_cache
@cross_domain_ajax
def ajax_login(request):
    """Ajax login."""
    if request.method == 'POST':
        response = {'success': False, 'data': {}}
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            request.session.set_expiry(86400)
            login(request, user)
            request.session['user_id'] = user.id
            response['success'] = True
            roles = request.user.groups.values_list('name', flat=True)
            response['data']['roles'] = list(roles)

        return HttpResponse(json.dumps(response),
                            content_type='application/json')
    else:
        return HttpResponse('Unauthorized', status=401)


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
                        SELECT id, observation_date::date as d, private_webmap_layer as c
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
def get_hashtags(request):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        hashtags = post_data['hashtags'].split(',')
        NOTES = []
        for h in hashtags:
            formatHashtag =  h if h.startswith('#') else ('#' + h)
            wordHashtag =  h + ' '
            NOTES.append(" NOTE ILIKE '%{}%'".format(wordHashtag))
            NOTES.append(" NOTE ILIKE '%{}'".format(formatHashtag))
        notes_str = ' OR '.join(NOTES)
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
					  SELECT id, observation_date::date as d, private_webmap_layer as c, report_id
					) As l
				  )) As properties
				   FROM map_aux_reports
				   WHERE lat is not null and lon is not null AND ({notes_str})
				   ORDER BY observation_date
			) As f
		) as features
        """

    with connection.cursor() as cursor:
        cursor.execute(SQL)
        data = cursor.fetchall()[0]
        # data = serialize("json", cursor.fetchone())

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

def doContinent(request, layer, continent, z, x, y):
    return doTile(request, layer, z, x, y, continent)

def doTile(request, layer, z, x, y, continent = None):
    CACHE_DIR = os.path.join(settings.MEDIA_ROOT,'cache')
    tilefolder = "{}/{}/{}/{}".format(CACHE_DIR,layer,z,x)    
    tilepath = "{}/{}.pbf".format(tilefolder,y)

    if layer == 'gadm0':
        code = "id_0 as id" 
    else:
        if layer == 'gadm1':
            code = "gid_1 as id" 
        else:
            if layer == 'gadm2':
                code = "gid_2 as id"
            else:
                if layer == 'gadm4':
                    code = "gid_4 as id" 

    if continent is None:
        where = ''
    else:
        where = "WHERE CONTINENT ilike '%" + continent + "%'"

    query = """
        WITH mvtgeom AS
        (
            SELECT {0},
                ST_AsMVTGeom(
                ST_Transform(geom, 3857),
                ST_TileEnvelope({2}, {3}, {4})
            ) AS geom
            FROM  {1} {5}
        )
        SELECT ST_AsMVT(mvtgeom.*)
        FROM   mvtgeom
        """.format(code, layer, z, x, y, where)

    cursor = connection.cursor()
    cursor.execute(query)
    tile = bytes(cursor.fetchone()[0])

    if not os.path.exists(tilefolder):
        os.makedirs(tilefolder)

    with open(tilepath, 'wb') as f:
        f.write(tile)
        f.close()

    cursor.close()

    # if not len(tile):
    #     raise Http404()

    return HttpResponse(tile, content_type="application/x-protobuf")


def availableModels(request):
    response = {}
    response['vector'] = {}
    response['biting'] = {}

    filename = BITES_FILE_NAME + BITES_FILE_EXTENSION
    response['biting'] = get_directory_structure(BITES_MODEL_FOLDER, filename)

    isVectorDataAvailable = False
    filename = VECTORS_FILE_NAME + VECTORS_FILE_EXTENSION

    for v in VECTORS_MODEL_NAMES:
        path = VECTORS_MODEL_FOLDER / v
        response['vector'][v] = get_directory_structure(path, filename)

        if (len(response['vector'][v]) > 0):
            isVectorDataAvailable = True

    response['availableVectorData'] = isVectorDataAvailable

    return HttpResponse(json.dumps(response),
                        content_type='application/json')

