from django.urls import path
from . import views

urlpatterns = [
    path('', views.mis_reservas, name='mis_reservas'),
    path('crear/', views.crear_reserva, name='crear_reserva'),
    path('crear/<int:habitacion_id>/', views.crear_reserva, name='crear_reserva_hab'),
    path('<int:reserva_id>/confirmacion/', views.confirmacion_reserva, name='confirmacion_reserva'),
    path('<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
]
