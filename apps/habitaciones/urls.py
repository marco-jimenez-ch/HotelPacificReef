from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('habitaciones/', views.lista_habitaciones, name='lista_habitaciones'),
    path('habitaciones/<int:pk>/', views.detalle_habitacion, name='detalle_habitacion'),
]
