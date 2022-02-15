"""API urls."""
from django.urls import path
from .views import get_feature, get_observation


urlpatterns = [
    path('get_feature/<observation_id>/', get_feature),
    path('get_observation/<observation_id>/', get_observation)
    # path('admin/', admin.site.urls),
    # path('', include('api.urls'))
]
