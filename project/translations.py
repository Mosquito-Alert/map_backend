from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.utils import translation

a = ("Open", "Layers")


def translations(request, lang):
    translation.activate(lang)
    return JsonResponse({
        # General
        "Open": _("Open"),
        "Close": _("Close"),
        # Mosquito types
        "Tiger mosquito": _("Tiger mosquito"),
        # Left drawer, Toolbar
        "Layers": _("Layers"),
        "Models": _("Models"),
        "Lang": _("Lang"),
        "Share": _("Share"),
        "Help": _("Help"),
        "Log in": _("Log in"),
        # Map, Popup
        "Date": _("Date"),
        "Expert note": _("Expert note"),
        "Confirmed": _("Confirmed"),
        "Probable": _("Probable")
    })
