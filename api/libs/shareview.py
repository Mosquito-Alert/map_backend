"""Userfixes Libraries."""
from datetime import datetime, date
import json
from django.http import JsonResponse
from api.models import MapView
import random
import string
import json

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


class ShareViewManager():
    """Main Observations Downloads Library."""  

    def __init__(self):
        """Constructor."""
        
        self.data = None

    def get_random_string(self, length):
        """Generates a new unique code for views"""
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def save(self, request):
        """Save view param into models."""
        self.data = request.body.decode("utf-8")
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
        
    def load(self, code):
        """Loads view params by code from models"""
        try:
            qs = MapView.objects.filter(
                code__exact=code
            ).values('code','view', 'date')[:1]

        except Exception as e:
            return JsonResponse({ "status": "error", "msg": str(e) })
        else:
            # view = serialize('json', qs, fields=('code','view','date',))
            print(list(qs))
            view = json.dumps(list(qs), default=json_serial)
            view = json.loads(view)
            return JsonResponse({ "status": "ok", "view": view })