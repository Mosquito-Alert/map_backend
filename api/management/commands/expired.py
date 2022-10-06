from django.core.management.base import BaseCommand, CommandError
from api.models import AppSettings, MapView, ReportView
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Remove expired shared views from database. Check for key days_to_expired_shared_views in database'

    def handle(self, *args, **options):
        info = AppSettings.objects.filter(key__exact="days_to_expired_shared_views").values('value').first()
        valid_date = datetime.now() - timedelta(days=int(info['value']))
        aware_datetime = make_aware(valid_date)

        qs = MapView.objects.filter(date__lte=aware_datetime)
        print("%d shared views have been deleted" % qs.count())
        qs.delete()

        qs = ReportView.objects.filter(date__lte=aware_datetime)
        print("%d shared reports have been deleted" % qs.count())
        qs.delete()

        
        