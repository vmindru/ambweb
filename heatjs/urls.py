from django.urls import path

from . import views

urlpatterns = [
    path('', views.heat_json),
    path('<heat_id>', views.heat_json),
]
