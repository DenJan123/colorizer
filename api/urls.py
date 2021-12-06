from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "api"

urlpatterns = [
    path("modify-color/", views.modify_color),
    path("convert-color/", views.convert_color),
    path("color-harmony/", views.color_harmony)
]
urlpatterns = format_suffix_patterns(urlpatterns)
