"""API urls."""
from django.urls import path, re_path
from .views import get_feature, get_observation, get_report, userfixes

re_date = '\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$'


urlpatterns = [
    path('get_feature/<observation_id>/', get_feature),
    path('get_observation/<observation_id>/', get_observation),
    path('get_reports/<report_id>/', get_report),
    re_path('userfixes/(?P<startdate>' + re_date + ')/(?P<enddate>' + re_date + ')/?$', userfixes)
]