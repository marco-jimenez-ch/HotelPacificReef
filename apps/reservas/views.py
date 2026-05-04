from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reserva
from .forms import ReservaForm
from apps.habitaciones.models import Habitacion


@login_required
def crear_reserva(request, habitacion_id=None):
    habitacion = None
    if habitacion_id:
        habitacion = get_object_or_404(Habitacion, pk=habitacion_id, disponible=True)

    initial = {}
    if habitacion:
        initial['habitacion'] = habitacion
    if request.GET.get('fecha_entrada'):
        initial['fecha_entrada'] = request.GET['fecha_entrada']
    if request.GET.get('fecha_salida'):
        initial['fecha_salida'] = request.GET['fecha_salida']

    form = ReservaForm(request.POST or None, initial=initial)
    if form.is_valid():
        reserva = form.save(commit=False)
        reserva.cliente = request.user
        reserva.save()
        messages.success(request, f'Reserva #{reserva.id} creada. Procede al pago de la garantía.')
        return redirect('resumen_pago', reserva_id=reserva.id)

    return render(request, 'reservas/crear.html', {'form': form, 'habitacion': habitacion})


@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(cliente=request.user).select_related('habitacion')
    return render(request, 'reservas/mis_reservas.html', {'reservas': reservas})


@login_required
def confirmacion_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id, cliente=request.user)
    return render(request, 'reservas/confirmacion.html', {'reserva': reserva})


@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id, cliente=request.user)
    if reserva.estado not in ['confirmada', 'pendiente']:
        messages.error(request, 'Esta reserva no puede cancelarse.')
        return redirect('mis_reservas')
    if request.method == 'POST':
        reserva.estado = 'cancelada'
        reserva.save()
        messages.warning(request, f'Reserva #{reserva.id} cancelada.')
        return redirect('mis_reservas')
    return render(request, 'reservas/cancelar.html', {'reserva': reserva})
# Épica 2: Registro de reserva por días — HU-06, RF-05
