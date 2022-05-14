"""Userfixes Libraries."""
from datetime import datetime
from django.conf import settings
import json
from django.http import JsonResponse
from api.models import MapView

class ShareViewManager():
    """Main Observations Downloads Library."""  

    def __init__(self, request):
        """Constructor."""

        self.data = json.loads(request.body.decode("utf-8"))       

    def save(self):
        try:
            view_instance = MapView.objects.create(view=self.data, date=datetime.now())
        except Exception as e:
            return JsonResponse({ "status": "error" })
        else:
            return JsonResponse({ "status": "ok" })
        
