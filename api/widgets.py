from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe

class MapWidget(Widget):
    # template_name = 'widgets/my_widget.html'
    template_name = "api/openlayers.html"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = args
        # Perquè peta això?

    class Media:
        css = {
            "all": (
                "https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.css",
                "https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css",
                "gis/css/ol3.css",
                "gis/css/widget-map.css",
            )
        }
        js = (
            "https://code.jquery.com/jquery-3.2.1.slim.min.js",
            "https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js",
            "https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.js",
            "gis/js/OLMapWidget.js",
            "gis/js/tileEvents.js",
        )

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)

        # Used on openlayers.html template
        context["id"] = "id"

        # I perquè això no peta?
        # print(self.urls[0])

        context["url"] = self.url[0]['url']

        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)