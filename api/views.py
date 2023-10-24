from django.views.decorators.csrf import csrf_exempt, csrf_protect
import random
from re import M
from django.http import JsonResponse, HttpResponse
from .models import MapAuxReport
from django.core.serializers import serialize
import json
from http import HTTPStatus
from django.db import connection
from .libs.userfixes import UserfixesManager
from .libs.downloads import DownloadsManager
from .libs.shareview import ShareViewManager
from .libs.reportview import ReportManager
import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.utils.cache import patch_cache_control, patch_response_headers
from django.views.decorators.cache import never_cache, cache_page
from django.views.decorators.vary import vary_on_cookie
from django.http import HttpResponseForbidden
from .decorators import session_cookie_required
from .libs.boundingBox import tile_bbox
from .constants import (public_fields, private_fields,
                        private_layers, public_layers)

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

ACC_HEADERS = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
               'Access-Control-Max-Age': 1000,
               'Access-Control-Allow-Headers': '*'}

def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response


@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

    login(request, user)
    return JsonResponse({'detail': 'Successfully logged in.'})


def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out.'})


@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False}, status = HTTPStatus.OK)

    return JsonResponse({'isAuthenticated': True}, status = HTTPStatus.OK)


def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'username': request.user.username})


@never_cache
@session_cookie_required
def downloads(request, fext):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        manager = DownloadsManager(request)
        if (fext == 'features'):
            return manager.getGeoJson(post_data)
        else:
            return manager.get(post_data, fext)

# Share Map View
@session_cookie_required
def saveView(request):
    if request.method == "POST":
        manager = ShareViewManager()
        return manager.save(request)

@session_cookie_required
def loadView(request, code):
    if request.method == "GET":
        manager = ShareViewManager()
        return manager.load(code)

# Map Report
@session_cookie_required
def saveReport(request):
    if request.method == "POST":
        manager = ReportManager()
        return manager.save(request)

@session_cookie_required
def loadReport(request, code):
    if request.method == "GET":
        manager = ReportManager()
        return manager.load(code)

@vary_on_cookie
@session_cookie_required
def get_data(request, year):

    layers = public_layers
    if request.user.is_authenticated:
        layers += private_layers

    return get_data_fields(request=request, year=year, map_layers=layers)

@cache_page(3600*2)
@session_cookie_required
def get_data_fields(request, year, map_layers):
    """Get data observations as geojson for the requested year."""

    map_layers_str = ', '.join(f"'{l}'" for l in map_layers)

    SQL = f"""
        SELECT jsonb_build_object(
            'year', {year},
            'type',     'FeatureCollection',
            'features', coalesce(jsonb_agg(features.feature), '[]')
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
                        AND PRIVATE_WEBMAP_LAYER IN ({map_layers_str})
                    ORDER BY observation_date
            ) As f
        ) as features
    """

    try:
        cursor = connection.cursor()
        cursor.execute(SQL)
        data = cursor.fetchall()[0]

    except Exception as e:
        response = JsonResponse({ "status": "error", "msg": str(e) }, status = HTTPStatus.BAD_GATEWAY)
    else:
        response = HttpResponse(data, content_type="application/json", status = HTTPStatus.OK)

    # Set Cache-Control response depending if there's any
    # private layer on the result or not.
    if set(map_layers).isdisjoint(private_layers):
        # Case only public layers.
        patch_cache_control(response, public=True)
    else:
        # Case at least one private layer.
        patch_cache_control(response, private=True)

    # Force Cache-Control header timeout (not set on private by default)
    patch_response_headers(response, cache_timeout=3600*2)

    return response


@csrf_exempt
@session_cookie_required
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
        try:
            cursor.execute(SQL)
            data = cursor.fetchall()[0]
        except Exception as e:
            return JsonResponse({ "status": HTTPStatus.BAD_GATEWAY, "msg": str(e) }, status = HTTPStatus.BAD_REQUEST)

    return HttpResponse(data, content_type="application/json", status = HTTPStatus.OK)


@csrf_exempt
@session_cookie_required
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
        try:
            cursor.execute(SQL)
            data = cursor.fetchall()[0]
        except Exception as e:
            return JsonResponse({ "status": HTTPStatus.BAD_GATEWAY, "msg": str(e) }, status = HTTPStatus.BAD_REQUEST)

        # data = serialize("json", cursor.fetchone())

    return HttpResponse(data, content_type="application/json", status = HTTPStatus.OK)

@session_cookie_required
def get_observation(request, observation_id):
    try:
        if request.user.is_authenticated:
            qs = MapAuxReport.objects.values(*(private_fields + public_fields)).get(pk = observation_id)
        else: 
            qs = MapAuxReport.objects.values(*public_fields).get(pk = observation_id)

        r = qs
        r['responses_json'] = json.loads(r['responses_json'])
        if (r['type'].lower() in ['bite', 'site']):
            r['formatedResponses'] = getFormatedResponses(r['type'], r['responses_json'], r['private_webmap_layer'])
    except Exception as e:
        return JsonResponse({ "status": "error", "msg": str(e) }, status = HTTPStatus.BAD_REQUEST)
    else:
        return HttpResponse(json.dumps(r, default=str), content_type="application/json", status = HTTPStatus.OK)

@session_cookie_required
def get_observation_by_id(request, id):
    try:
        if request.user.is_authenticated:
            qs = MapAuxReport.objects.values(*(private_fields + public_fields)).get(version_uuid = id)
        else: 
            qs = MapAuxReport.objects.values(*public_fields).get(version_uuid = id)
    except Exception as inst:
        return JsonResponse({'status': 'error', 'error': str(inst)}, status = HTTPStatus.BAD_REQUEST)

    r = qs
    r['responses_json'] = json.loads(r['responses_json'])
    if (r['type'].lower() in ['bite', 'site']):
        r['formatedResponses'] = getFormatedResponses(r['type'], r['responses_json'], r['private_webmap_layer'])

    return HttpResponse(json.dumps(r, default=str), content_type="application/json", status = HTTPStatus.OK)

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

@cache_page(86400)
@session_cookie_required
def userfixes_all(request, **filters):
    """Get Coverage Layer Info."""
    manager = UserfixesManager(request)
    params = { 'startdate': None, 'enddate': None }
    return manager.get('GeoJSON', **params)

@cache_page(86400)
@session_cookie_required
def userfixes(request, **filters):
    """Get Coverage Layer Info."""
    manager = UserfixesManager(request)
    return manager.get('GeoJSON', **filters)

def doContinent(request, layer, continent, z, x, y):
    return doTile(request, layer, z, x, y, continent)

@session_cookie_required
def doTile(request, layer, z, x, y, continent = None):
    CACHE_DIR = os.path.join(settings.MEDIA_ROOT,'tiles')
    tilefolder = "{}/{}/{}/{}".format(CACHE_DIR,layer,z,x)
    tilepath = "{}/{}.pbf".format(tilefolder,y)

    if layer == 'gadm0':
        code = "gid_0 as id" 
    else:
        if layer == 'gadm1':
            code = "gid_1 as id" 
        else:
            if layer == 'gadm2':
                code = "gid_2 as id"
            else:
                if layer == 'gadm3':
                    code = "gid_3 as id" 
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