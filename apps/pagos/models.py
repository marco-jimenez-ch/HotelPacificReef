from django.db import models
from apps.reservas.models import Reserva

class Pago(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('rechazado', 'Rechazado'),
    ]
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    monto_garantia = models.DecimalField(max_digits=10, decimal_places=0)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    codigo_qr = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    codigo_transaccion = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f"Pago Reserva #{self.reserva.id} — ${self.monto_garantia}"
