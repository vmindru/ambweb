from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.heat),
    re_path(r'^json/$', views.heat_json),
    re_path(r'^ref/$', views.heat_refresh),
]
