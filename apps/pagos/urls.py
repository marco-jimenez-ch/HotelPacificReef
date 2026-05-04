from django.urls import path
from . import views

urlpatterns = [
    path('<int:reserva_id>/resumen/', views.resumen_pago, name='resumen_pago'),
    path('<int:reserva_id>/procesar/', views.procesar_pago, name='procesar_pago'),
    path('<int:reserva_id>/comprobante/', views.comprobante_qr, name='comprobante_qr'),
]
