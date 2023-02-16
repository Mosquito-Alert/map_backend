"""API urls."""
from django.urls import path, re_path
from . import views

re_date = '\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])'


urlpatterns = [
    # path('get_observation/<observation_id>/', get_observation),
    re_path('get/data/(?P<year>(\d{4}))/$', views.get_data),
    re_path('get_observation/(?P<observation_id>(\d*))/$', views.get_observation),
    re_path('get_observation/(?P<id>[\-a-zA-Z0-9]{36})/$', views.get_observation_by_id),
    re_path('downloads/(?P<fext>(xlsx|gpkg|features))/$', views.downloads),
    re_path('view/load/(?P<code>[a-zA-Z0-9\-]{4,6})/$', views.loadView),
    re_path('report/load/(?P<code>[a-zA-Z0-9]{6})/$', views.loadReport),
    re_path('userfixes/(?P<startdate>' + re_date + ')/(?P<enddate>' + re_date + ')/?$', views.userfixes),
    re_path('userfixes/?$', views.userfixes_all),
    path('get_reports/', views.get_reports),
    path('get_hashtags/', views.get_hashtags),
    path('view/save/', views.saveView),
    path('report/save/', views.saveReport),
    path('tiles/<str:layer>/<int:z>/<int:x>/<int:y>.pbf', views.doTile),
    path('tiles/<str:layer>/<str:continent>/<int:z>/<int:x>/<int:y>', views.doContinent),
    # path('login/', ajax_login),
    # path('logout/', ajax_logout),
    path('csrf/', views.get_csrf, name='api-csrf'),
    path('login/', views.login_view, name='api-login'),
    path('logout/', views.logout_view, name='api-logout'),
    path('session/', views.session_view, name='api-session'),
    path('whoami/', views.whoami_view, name='api-whoami'),
]