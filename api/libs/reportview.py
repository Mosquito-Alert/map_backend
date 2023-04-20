"""Userfixes Libraries."""
from datetime import datetime, date
import json
from django.http import JsonResponse
from api.models import ReportView
import random
import string
import json
from http import HTTPStatus

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


class ReportManager():
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
                    random_code = self.get_random_string(6)
                    qs = ReportView.objects.filter(code__exact=random_code)
                    if qs.count() == 0:
                        break
                except Exception as e:
                    return JsonResponse({ "status": HTTPStatus.BAD_REQUEST, "msg": str(e) }, status = HTTPStatus.BAD_REQUEST)

            view_instance = ReportView.objects.create(
                view=self.data,
                date=datetime.now(),
                code=random_code
            )

        except Exception as e:
            return JsonResponse({ "status": HTTPStatus.BAD_REQUEST, "msg": str(e) }, status = HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({ "status": HTTPStatus.OK, "code": random_code }, status = HTTPStatus.OK)

    def load(self, code):
        """Loads view params by code from models"""
        try:
            qs = ReportView.objects.filter(
                code__exact=code
            ).values('code','view', 'date')[:1]

            if qs.count() == 0:
                raise Exception('This report does not exist')

        except Exception as e:
            return JsonResponse({ "status": HTTPStatus.BAD_REQUEST, "msg": str(e) }, status = HTTPStatus.BAD_REQUEST)
        else:
            # view = serialize('json', qs, fields=('code','view','date',))
            view = json.dumps(list(qs), default=json_serial)
            view = json.loads(view)
            return JsonResponse({ "status": HTTPStatus.OK, "view": view }, status = HTTPStatus.OK)