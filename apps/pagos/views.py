from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.reservas.models import Reserva
from .models import Pago
from .utils import calcular_garantia, generar_codigo_qr, generar_codigo_transaccion


@login_required
def resumen_pago(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id, cliente=request.user)
    garantia = calcular_garantia(reserva.costo_total)
    pago_existente = getattr(reserva, 'pago', None)

    if pago_existente and pago_existente.estado == 'pagado':
        return redirect('comprobante_qr', reserva_id=reserva.id)

    return render(request, 'pagos/resumen_pago.html', {
        'reserva': reserva,
        'garantia': garantia,
    })


@login_required
def procesar_pago(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id, cliente=request.user)

    if reserva.estado == 'cancelada':
        messages.error(request, 'No se puede pagar una reserva cancelada.')
        return redirect('mis_reservas')

    pago_existente = getattr(reserva, 'pago', None)
    if pago_existente and pago_existente.estado == 'pagado':
        messages.info(request, 'El pago ya fue procesado.')
        return redirect('comprobante_qr', reserva_id=reserva.id)

    if request.method == 'POST':
        garantia = calcular_garantia(reserva.costo_total)
        codigo = generar_codigo_transaccion()

        qr_data = {
            'id': reserva.id,
            'cliente': reserva.cliente.get_full_name() or reserva.cliente.username,
            'habitacion': str(reserva.habitacion),
            'fecha_entrada': reserva.fecha_entrada,
            'fecha_salida': reserva.fecha_salida,
            'garantia': int(garantia),
            'codigo_transaccion': codigo,
        }
        archivo_qr = generar_codigo_qr(qr_data)

        if pago_existente:
            pago = pago_existente
        else:
            pago = Pago(reserva=reserva)

        pago.monto_garantia = garantia
        pago.estado = 'pagado'
        pago.fecha_pago = timezone.now()
        pago.codigo_transaccion = codigo
        pago.codigo_qr.save(archivo_qr.name, archivo_qr, save=False)
        pago.save()

        reserva.estado = 'confirmada'
        reserva.save()

        messages.success(request, '¡Pago procesado exitosamente! Tu reserva está confirmada.')
        return redirect('comprobante_qr', reserva_id=reserva.id)

    return redirect('resumen_pago', reserva_id=reserva.id)


@login_required
def comprobante_qr(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id, cliente=request.user)
    pago = get_object_or_404(Pago, reserva=reserva)
    return render(request, 'pagos/comprobante_qr.html', {
        'reserva': reserva,
        'pago': pago,
    })
# Épica 3: Pagos y Confirmaciones — HU-07, HU-08, RF-06, RF-07
