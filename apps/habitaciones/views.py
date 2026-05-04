from django.shortcuts import render, get_object_or_404
from .models import Habitacion
from apps.reservas.models import Reserva
from datetime import date


def home(request):
    habitaciones_destacadas = Habitacion.objects.filter(disponible=True)[:3]
    return render(request, 'home.html', {'habitaciones': habitaciones_destacadas})


def lista_habitaciones(request):
    tipo_filtro = request.GET.get('tipo', '')
    fecha_entrada = request.GET.get('fecha_entrada', '')
    fecha_salida = request.GET.get('fecha_salida', '')

    habitaciones = Habitacion.objects.filter(disponible=True)
    if tipo_filtro:
        habitaciones = habitaciones.filter(tipo=tipo_filtro)

    return render(request, 'habitaciones/lista.html', {
        'habitaciones': habitaciones,
        'tipo_filtro': tipo_filtro,
        'fecha_entrada': fecha_entrada,
        'fecha_salida': fecha_salida,
    })


def detalle_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    return render(request, 'habitaciones/detalle.html', {
        'habitacion': habitacion,
        'hoy': date.today().isoformat(),
    })
