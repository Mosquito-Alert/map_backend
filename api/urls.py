"""API urls."""
from django.urls import path, re_path
from .views import (saveView, loadView, saveReport, loadReport, downloads,
                    get_feature, get_observation, get_observation_by_id,
                    get_data, get_reports, userfixes, doTile, doContinent,
                    availableModels)

re_date = '\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])'


urlpatterns = [
    path('get_feature/<observation_id>/', get_feature),
    # path('get_observation/<observation_id>/', get_observation),
    path('get_reports/', get_reports),
    path('view/save/', saveView),    
    path('report/save/', saveReport),    
    re_path('get_observation/(?P<observation_id>(\d*))/$', get_observation),
    re_path('get_observation/(?P<id>[\-a-zA-Z0-9]{36})/$', get_observation_by_id),
    re_path('get/data/(?P<year>(\d{4}))/$', get_data),
    re_path('downloads/(?P<fext>(xlsx|gpkg|features))/$', downloads),
    re_path('view/load/(?P<code>[a-zA-Z0-9]{4})/$', loadView),    
    re_path('report/load/(?P<code>[a-zA-Z0-9]{6})/$', loadReport),    
    re_path('userfixes/(?P<startdate>' + re_date + ')/(?P<enddate>' + re_date + ')/?$', userfixes),
    path('tiles/<str:layer>/<int:z>/<int:x>/<int:y>', doTile),
    path('tiles/<str:layer>/<str:continent>/<int:z>/<int:x>/<int:y>', doContinent),
    path('models/available/', availableModels)
]