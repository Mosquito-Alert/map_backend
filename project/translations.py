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
        "Filter": _("Filter"),

        # observation categories
        "mosquito_tiger_probable": _("mosquito tiger probable"),
        "breeding_site_not_yet_filtered": _("breeding site not yet filtered"),
        "conflict": _("conflict"),
        "mosquito_tiger_confirmed": _("mosquito tiger confirmed"),
        "unidentified": _("unidentified"),
        "yellow_fever_confirmed": _("yellow fever confirmed"),
        "storm_drain_water": _("storm drain water"),
        "breeding_site_other": _("breeding site other"),
        "other_species": _("other species"),
        "storm_drain_dry": _("storm drain dry"),
        "not_yet_validated": _("not yet validated"),
        "yellow_fever_probable": _("yellow fever probable"),
        "trash_layer": _("trash layer"),

        # Mosquito types
        "tiger mosquito": _("Tiger mosquito"),
        "tiger": _("Tiger mosquito"),
        "yellow fever mosquito": _("yellow fever mosquito"),
        "yellow": _("yellow fever mosquito"),
        "japonicus mosquito": _("japonicus mosquito"),
        "japonicus": _("japonicus mosquito"),
        "koreicus mosquito": _("koreicus mosquito"),
        "koreicus": _("koreicus mosquito"),
        "culex mosquito": _("culex mosquito"),
        "culex": _("culex mosquito"),
        "unidentified mosquito": _("unidentified mosquito"),
        "unidentified": _("unidentified mosquito"),
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
        "Probable": _("Probable"),
        "Expert validation": _("Expert validation"),
        "AI validation": _("AI validation"),
        # Timeseries
        "Pick a date range": _("Pick a date range")
    })
