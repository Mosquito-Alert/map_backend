from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.utils import translation

a = ("Open", "Layers")


def translations(request, lang):
    translation.activate(lang)
    return JsonResponse({
        # General
        "Shown points": _("Shown points"),
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
        "Continue": _("Continue"),

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
        "Mosquito japonicus/koreicus": _("Mosquito japonicus/koreicus"),
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
        "Breeding site other": _("Breeding site other"),
        
        # other observations
        "Other species": _("Other species"),
        
        # Left drawer, Toolbar
        "Layers": _("Layers"),
        "Models": _("Models"),
        "Lang": _("Lang"),
        "Share": _("Share"),
        "Help": _("Help"),
        "Log in": _("Log in"),
        
        # Timeseries
        "Time series": _("Time series"),
        "Pick a date range": _("Pick a date range"),
        "Delete calendar": _("Delete calendar"),
        "Apply calendar": _("Apply calendar"),

        # Map, Popup
        'Anonymous': _("Anonymous"),
        'How many bites': _("How many bites"),
        'Body part': _("Body part"),
        'Bite location': _("Bite location"),   
        'Bite time': _("Bite time"),   

        "Date": _("Date"),
        "Expert note": _("Expert note"),
        "Confirmed": _("Confirmed"),
        "Probable": _("Probable"),
        "Expert validation": _("Expert validation"),
        "AI validation": _("AI validation"),

        'Unknown': _("_Unknown"),
        'Outdoors': _("Outdoors"),
        'Inside building': _("Inside building"),
        'inside vehicle': _("Inside vehicle"),
        'At sunrise': _("At sunrise"),
        'At noon': _("At noon"),
        'At sunset': _("At sunset"),
        'At night': _("At night"),
        'Not really sure': _("Not really sure"),
    
        'Head':  _("Head"),
        'Left arm': _("Left arm"),
        'Right arm': _("Right arm"),
        'Chest': _("Chest"),
        'Left leg': _("Left leg"),
        'Right leg': _("Right leg"),
    
        'Breeding site with water': _("Breeding site with water"),
        'Breeding site without water': _("Breeding site without water"),
        'Breeding site with larva': _("Breeding site with larva"),
        'No': _("No"),
        'Yes': _("Yes"),

        'Not available':_("Not available"),
        'No results found': _("No results found"),

        # Download
        'Download': _("Download"),
        'Download geopackage': _("Download geopackage"),
        'Download excel': _("Download excel"),
        'No features to download': _("No features to download"),
        'Only data displayed in the current map view will be downloaded. Verify your current active layers, temporal filters and zoom.': _("Only data displayed in the current map view will be downloaded. Verify your current active layers, temporal filters and zoom."),
        'Once verified, press the download button.': _("Once verified, press the download button."),
        'For the Mosquito Alert complete dataset, with advanced options, go to Mosquito Alert portal: http://www.mosquitoalert.com/en/access-to-mosquito-alert-data-portal/': _("For the Mosquito Alert complete dataset, with advanced options, go to Mosquito Alert portal: http://www.mosquitoalert.com/en/access-to-mosquito-alert-data-portal/"),   
    
        # Share view
        'This is the new view url': _("This is the new view url"),
        'This view does not exist': _("This view does not exist"),
        'Share modal title': _("Share modal title"),
        'Share this map view': _("Share this map view"),

        # Reports / modal
        'Coordinates (latitud, longitud)': _("Coordinates (latitud, longitud)"),
        'Reports': _("Reports"),
        'Reports limit exceeded': _("Reports limit exceeded"),
        'List of observations':_("List of observations"),       
        'Selected observations': _("Selected observations"),
        'Filters applied': _("Filters applied"),
        'Reports modal title': _("Reports modal title"),
        'Report with the observations displayed in the current map view (maximum: 300 observations)': _("Report with the observations displayed in the current map view (maximum: 300 observations)"),
        'Verify this by looking at the map point counter': _("Verify this by looking at the map point counter (on the down left map corner).")

    })
