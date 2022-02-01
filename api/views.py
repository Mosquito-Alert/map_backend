import random
from django.shortcuts import render
from django.templatetags.static import static
from django.http import JsonResponse


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
        data["img"] = 'http://localhost:8000/static/api/mosquito/dummy.jpg'
    return JsonResponse(data)
