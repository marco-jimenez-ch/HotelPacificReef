from django.contrib import admin
from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'habitacion', 'fecha_entrada', 'fecha_salida', 'estado', 'costo_total']
    list_filter = ['estado', 'habitacion__tipo']
    search_fields = ['cliente__username', 'habitacion__numero']
    readonly_fields = ['fecha_creacion']
