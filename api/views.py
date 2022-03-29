import random
from re import M
from django.shortcuts import render
from django.templatetags.static import static
from django.http import JsonResponse, HttpResponse
from .models import MapAuxReport
from django.core.serializers import serialize
import json

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

def get_observation(request, observation_id):
    qs = MapAuxReport.objects.get(pk = observation_id)
    data = serialize("json", [qs])
    r = json.loads(data)[0]['fields']
    r['responses_json'] = json.loads(r['responses_json'])
    if (r['type'].lower() in ['bite', 'site']):
        r['formatedResponses'] = getFormatedResponses(r['type'], r['responses_json'])
    return HttpResponse(json.dumps(r), content_type="application/json")

def getValueOrNull(key, values):
    key = str(key)
    if key in values:
        return values[key]
    else:
        return 'unkown'

def getFormatedResponses(type, responses):
    locations = {
        '44': 'unknown', '43': 'outdoors',
        '42': 'inside building','41': 'inside vehicle'
    }
    biteTimes = {
        '31': 'at sunrise', '32': 'at noon',
        '33': 'at sunset', '34': 'at night',
        '35': 'not really sure'
    }
    bodyParts = {
        '21': 'head', '22': 'left arm',
        '23': 'right arm', '24': 'chest',
        '25': 'left leg', '26': 'right leg'
    }
    siteTipologies = {
        '101': 'breeding site with water',
        '81': 'breeding site without water'
    }
    withLarva = { '81': 'no', '101': 'yes' }

    NUMBER_OF_BITES = 1
    WHERE_DID_THEY_BITE_YOU = 4
    BITE_TIME = 3
    BODY_PART_BITTEN = 2
    SITE_WATER_STATUS = 10
    SITE_LARVA_STATUS = 17
    formated = {}

    if type.lower() == 'bite':
        for response in responses:
            if response['question_id'] == NUMBER_OF_BITES:
                formated['howManyBites'] = response['answer_id']

            elif response['question_id'] == WHERE_DID_THEY_BITE_YOU:              
                formated['location'] = getValueOrNull(response['answer_id'], locations)

            elif response['question_id'] == BITE_TIME:
                formated['biteTime'] = getValueOrNull(response['answer_id'], biteTimes)

            elif response['question_id'] == BODY_PART_BITTEN:
                formated['bodyPart'] = getValueOrNull(response['answer_id'], bodyParts)
                
    else:
        for response in responses:
            if response['question_id'] == SITE_WATER_STATUS:
                formated['siteTipology'] = getValueOrNull(response['answer_id'], siteTipologies)

            if response['question_id'] == SITE_LARVA_STATUS:
                formated['withLarva'] = getValueOrNull(response['answer_id'], withLarva)
    
    return formated