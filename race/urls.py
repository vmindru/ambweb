from django.urls import path

from . import views

urlpatterns = [
    path('', views.heat),
    path('<int:heat_id>/', views.heat_by_id),
    path('<int:heat_id>/<int:kart_id>', views.heat_kart),
]
