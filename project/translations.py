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
        "select": _("select"),
        "mosquitos": _("mosquitos"),
        "bites": _("bites"),
        "breeding sites": _("breeding sites"),
        "sampling effort": _("sampling effort"),
        "placeholder location": _("placeholder location"),
        "placeholder hashtag": _("placeholder hashtag"),

        # Mosquito types
        "tiger mosquito": _("Tiger mosquito"),
        "yellow fever mosquito": _("yellow fever mosquito"),
        "japonicus mosquito": _("japonicus mosquito"),
        "koreicus mosquito": _("koreicus mosquito"),
        "culex mosquito": _("culex mosquito"),
        "unidentified mosquito": _("unidentified mosquito"),
        "others_mosquito": _("others_mosquito"),

        # breeding sites
        "stormdrain with water": _("storm drain with water"),
        "stormdrain without water": _("storm drain without water"),
        "breeding site others": _("breeding site others"),
        # other observations
        "other species": _("other species"),
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
