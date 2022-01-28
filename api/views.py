from django.shortcuts import render
from django.http import JsonResponse


def get_feature(request, id):
    """Return a feature."""
    return JsonResponse({
        'layer': 'mosquito_tiger_confirmed',
        'date': '21-02-2021',
        'description': 'Blah, blah, blah',
        # 'img': 'empty'
    })
