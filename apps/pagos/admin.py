from django.contrib import admin
from .models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'reserva', 'monto_garantia', 'estado', 'fecha_pago', 'codigo_transaccion']
    list_filter = ['estado']
    search_fields = ['reserva__cliente__username', 'codigo_transaccion']
    readonly_fields = ['fecha_pago', 'codigo_transaccion']
