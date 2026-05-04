from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from apps.habitaciones.models import Habitacion

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    num_huespedes = models.IntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    @property
    def total_noches(self):
        return (self.fecha_salida - self.fecha_entrada).days

    @property
    def costo_total(self):
        return self.habitacion.precio_por_noche * self.total_noches

    @property
    def garantia_30(self):
        return self.costo_total * Decimal('0.30')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"Reserva #{self.id} — {self.cliente.username}"
