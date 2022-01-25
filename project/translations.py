from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.utils import translation


def translations(request, lang):
    translation.activate(lang)
    return JsonResponse({
        "Open": _("Open")
    })
