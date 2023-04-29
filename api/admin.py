from django.contrib import admin
# from .models import MapAuxReport, AppSettings
from .models import TabsStatus, WmsServer, WmsMapLayer
from .widgets import MapWidget, SliderWidget
from django import forms
from rest_framework.authtoken.models import Token

class TabsStatusAdmin(admin.ModelAdmin):
    list_display = ('tab','active')

class WmsMapLayerForm(forms.ModelForm):
    title = None
    wmsUrl = None

    def __init__(self, *args, **kwargs):
        # when adding record, no instance exists
        if kwargs.get('instance') is None:
            wmsUrl = None
        else:
            wmsUrl = kwargs['instance'].wms_server

        super().__init__(*args, **kwargs)

        # Pass whatever data you want to the widget constructor here
        self.fields['name'].widget = MapWidget({'url': wmsUrl})

    class Meta:
        model = WmsMapLayer
        widgets = {
            'name': MapWidget(),
            'transparency': SliderWidget(attrs={'type': 'range', 'class': 'form-range', 'min': '0', 'max': '1', 'step': '0.05'})
        }
        fields = '__all__' # required for Django 3.x


class WmsMapLayerAdmin(admin.ModelAdmin):
    form = WmsMapLayerForm

admin.site.register(WmsServer)
admin.site.register(WmsMapLayer, WmsMapLayerAdmin)
admin.site.register(TabsStatus, TabsStatusAdmin)
