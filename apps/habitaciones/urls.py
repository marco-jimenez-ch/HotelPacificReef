from django.urls import path
from . import views

urlpatterns = [
    # Vistas web
    path("", views.home, name="home"),
    path("habitaciones/", views.lista_habitaciones, name="lista_habitaciones"),
    path("habitaciones/<int:pk>/", views.detalle_habitacion, name="detalle_habitacion"),

    # API REST interna
    path("api/habitaciones/", views.api_habitaciones_lista, name="api_habitaciones"),
    path("api/habitaciones/<int:pk>/", views.api_habitacion_detalle, name="api_habitacion_detalle"),
    path("api/disponibilidad/", views.api_disponibilidad, name="api_disponibilidad"),
]