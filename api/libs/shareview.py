"""Userfixes Libraries."""
from datetime import datetime
from django.conf import settings
import json
from django.http import JsonResponse
from api.models import MapView
import random
import string


class ShareViewManager():
    """Main Observations Downloads Library."""  

    def __init__(self, request):
        """Constructor."""

        self.data = json.loads(request.body.decode("utf-8"))       

    def save(self):
        try:
            while True:
                try:
                    random_code = self.get_random_string(4)
                    qs = MapView.objects.filter(code__exact=random_code)
                    if qs.count() == 0:
                        break
                except Exception as e:
                    return JsonResponse({ "status": "error", "msg": str(e) })

            view_instance = MapView.objects.create(
                view=self.data,
                date=datetime.now(),
                code=random_code
            )

        except Exception as e:
            return JsonResponse({ "status": "error", "msg": str(e) })
        else:
            return JsonResponse({ "status": "ok", "code": random_code })
        
    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str