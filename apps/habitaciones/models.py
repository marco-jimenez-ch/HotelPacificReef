from django.db import models

class Habitacion(models.Model):
    TIPO_CHOICES = [
        ('individual', 'Individual'),
        ('doble', 'Doble'),
        ('suite', 'Suite'),
    ]
    numero = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    capacidad = models.IntegerField()
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=0)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='habitaciones/', blank=True, null=True)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Habitación'
        verbose_name_plural = 'Habitaciones'

    def __str__(self):
        return f"Hab. {self.numero} — {self.tipo} (${self.precio_por_noche}/noche)"
