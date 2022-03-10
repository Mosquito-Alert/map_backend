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
        "Select": _("Select"),
        "Mosquitos": _("Mosquitos"),
        "Bites": _("Bites"),
        "Breeding sites": _("Breeding sites"),
        "Sampling effort": _("Sampling effort"),
        "Placeholder location": _("Placeholder location"),
        "Placeholder hashtag": _("Placeholder hashtag"),
        "Filter": _("Filter"),

        # observation categories
        "Mosquito_tiger_probable": _("Mosquito tiger probable"),
        "Breeding_site_not_yet_filtered": _("Breeding site not yet filtered"),
        "Conflict": _("Conflict"),
        "Mosquito_tiger_confirmed": _("Mosquito tiger confirmed"),
        "Unidentified": _("Unidentified"),
        "Yellow_fever_confirmed": _("Yellow fever confirmed"),
        "Storm_drain_water": _("Storm drain water"),
        "Breeding_site_other": _("Breeding site other"),
        "Other_species": _("Other species"),
        "Storm_drain_dry": _("Storm drain dry"),
        "Not_yet_validated": _("Not yet validated"),
        "Yellow_fever_probable": _("Yellow fever probable"),
        "Trash_layer": _("Trash layer"),

        # Mosquito types
        "Tiger mosquito": _("Tiger mosquito"),
        "Tiger": _("Tiger mosquito"),
        "Yellow fever mosquito": _("Yellow fever mosquito"),
        "Yellow": _("Yellow fever mosquito"),
        "Japonicus mosquito": _("Japonicus mosquito"),
        "Japonicus": _("Japonicus mosquito"),
        "Koreicus mosquito": _("Koreicus mosquito"),
        "Koreicus": _("Koreicus mosquito"),
        "Culex mosquito": _("Culex mosquito"),
        "Culex": _("Culex mosquito"),
        "Unidentified mosquito": _("Unidentified mosquito"),
        "Unidentified": _("Unidentified mosquito"),
        "Others_mosquito": _("Others_mosquito"),

        # breeding sites
        "Stormdrain with water": _("Storm drain with water"),
        "Stormdrain without water": _("Storm drain without water"),
        "Breeding site others": _("Breeding site others"),
        # other observations
        "Other species": _("Other species"),
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
        "Time series": _("Time series"),
        "Pick a date range": _("Pick a date range")
    })
