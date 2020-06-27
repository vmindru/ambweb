from django.urls import path

from . import views

urlpatterns = [
    path('', views.laps_json),
    path('<heat_id>', views.laps_json),
]
