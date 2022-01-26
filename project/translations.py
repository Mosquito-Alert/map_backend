from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.utils import translation

words = ["Open"]
# Left drawer toolbar
words = words + [
    "Help", "Lang", "Layers", "Log in", "Models", "Share",
]


def translations(request, lang):
    translation.activate(lang)
    translated = {}
    for word in words:
        translated[word] = _(word)
    return JsonResponse(translated)
