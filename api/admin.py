from django.contrib import admin
# from .models import MapAuxReport, AppSettings
from .models import TabsStatus, WmsServer, WmsMapLayer
from .widgets import MapWidget
from django import forms

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
        }
        fields = '__all__' # required for Django 3.x


class WmsMapLayerAdmin(admin.ModelAdmin):
    form = WmsMapLayerForm

admin.site.register(WmsServer)
admin.site.register(WmsMapLayer, WmsMapLayerAdmin)
admin.site.register(TabsStatus, TabsStatusAdmin)