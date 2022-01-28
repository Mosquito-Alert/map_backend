"""API urls."""
from django.urls import path
from .views import get_feature


urlpatterns = [
    path('get_feature/<id>/', get_feature)
    # path('admin/', admin.site.urls),
    # path('', include('api.urls'))
]
