from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.utils import translation


def translations(request, lang):
    translation.activate(lang)
    return JsonResponse({
        "Open": _("Open"),
        "Layers": _("Layers"),
        "Models": _("Models"),
        "Lang": _("Lang"),
        "Share": _("Share"),
        "Help": _("Help"),
        "Log in": _("Log in")
    })
