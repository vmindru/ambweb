from django.urls import path

from . import views

urlpatterns = [
    path('', views.heat),
    path('debug/<int:heat_id>/', views.heat_id),
    path('debug/<int:heat_id>/<int:kart_id>', views.heat_kart),
]
