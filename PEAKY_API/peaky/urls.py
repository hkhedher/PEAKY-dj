from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='MOUNTAIN PEAKS API', url='/api/docs')

urlpatterns = [
    path("api/peaks", views.peak_list),
    path("api/peaks/<int:pk>/", views.peak_detail),
    path("api/peaks/<str:xmin>/<str:ymin>/<str:xmax>/<str:ymax>/", views.peaks_by_bbox),
    path("api/docs/", schema_view),
]
