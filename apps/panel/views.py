from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from apps.reservas.models import Reserva
from apps.habitaciones.models import Habitacion
from apps.pagos.models import Pago


def es_admin(user):
    perfil = getattr(user, 'perfil', None)
    return user.is_superuser or (perfil and perfil.rol == 'admin')


@login_required
def dashboard(request):
    if not es_admin(request.user):
        messages.error(request, 'Acceso restringido al panel administrativo.')
        return redirect('home')

    total_reservas = Reserva.objects.count()
    reservas_confirmadas = Reserva.objects.filter(estado='confirmada').count()
    reservas_pendientes = Reserva.objects.filter(estado='pendiente').count()
    reservas_canceladas = Reserva.objects.filter(estado='cancelada').count()

    ingresos = Pago.objects.filter(estado='pagado').aggregate(
        total=Sum('monto_garantia')
    )['total'] or 0

    habitaciones_disponibles = Habitacion.objects.filter(disponible=True).count()
    habitaciones_total = Habitacion.objects.count()

    reservas_recientes = Reserva.objects.select_related(
        'cliente', 'habitacion'
    ).order_by('-fecha_creacion')[:10]

    return render(request, 'panel/dashboard.html', {
        'total_reservas': total_reservas,
        'reservas_confirmadas': reservas_confirmadas,
        'reservas_pendientes': reservas_pendientes,
        'reservas_canceladas': reservas_canceladas,
        'ingresos': ingresos,
        'habitaciones_disponibles': habitaciones_disponibles,
        'habitaciones_total': habitaciones_total,
        'reservas_recientes': reservas_recientes,
    })


@login_required
def reportes(request):
    if not es_admin(request.user):
        messages.error(request, 'Acceso restringido al panel administrativo.')
        return redirect('home')

    ocupacion_por_tipo = Reserva.objects.filter(
        estado='confirmada'
    ).values('habitacion__tipo').annotate(
        total=Count('id')
    ).order_by('-total')

    ingresos_por_tipo = Pago.objects.filter(
        estado='pagado'
    ).values('reserva__habitacion__tipo').annotate(
        total=Sum('monto_garantia')
    ).order_by('-total')

    return render(request, 'panel/reportes.html', {
        'ocupacion_por_tipo': ocupacion_por_tipo,
        'ingresos_por_tipo': ingresos_por_tipo,
    })
