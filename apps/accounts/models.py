from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('cliente', 'Cliente'),
        ('admin', 'Administrador'),
    ]
    TIPO_DOC_CHOICES = [
        ('run', 'RUN'),
        ('pasaporte', 'Pasaporte'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')
    telefono = models.CharField(max_length=20, blank=True)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOC_CHOICES, default='run')
    rut = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'

    def __str__(self):
        return f"{self.usuario.get_full_name()} ({self.rol})"
