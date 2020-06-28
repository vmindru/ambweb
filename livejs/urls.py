from django.urls import path

from . import views

urlpatterns = [
    path('', views.live_json),
    path('<heat_id>', views.live_json),
]
