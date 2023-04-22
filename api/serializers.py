from rest_framework import serializers
from api.models import TabsStatus, WmsMapLayer

class WmsMapLayerSerializer(serializers.ModelSerializer):
  class Meta():
    model = WmsMapLayer
    fields = ('species','year','name')