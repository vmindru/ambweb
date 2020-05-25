from django.urls import path

from . import views

urlpatterns = [
    path('', views.heat_refresh),
    path('<heat_id>', views.heat_refresh),
]
