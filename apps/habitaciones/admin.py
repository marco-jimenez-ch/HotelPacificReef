from django.contrib import admin
from .models import Habitacion


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ['numero', 'tipo', 'capacidad', 'precio_por_noche', 'disponible']
    list_filter = ['tipo', 'disponible']
    search_fields = ['numero', 'descripcion']
    list_editable = ['disponible']
