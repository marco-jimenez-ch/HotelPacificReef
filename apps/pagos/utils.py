from decimal import Decimal
import qrcode
import io
import uuid
import base64
from django.core.files.base import ContentFile


def calcular_garantia(costo_total):
    return Decimal(str(costo_total)) * Decimal('0.30')


def generar_qr_base64(datos_reserva: dict) -> str:
    contenido = (
        f"HOTEL PACIFIC REEF\n"
        f"Reserva: #{datos_reserva['id']}\n"
        f"Cliente: {datos_reserva['cliente']}\n"
        f"Habitación: {datos_reserva['habitacion']}\n"
        f"Check-in: {datos_reserva['fecha_entrada']}\n"
        f"Check-out: {datos_reserva['fecha_salida']}\n"
        f"Garantía pagada: ${datos_reserva['garantia']}\n"
        f"Cód. transacción: {datos_reserva['codigo_transaccion']}"
    )
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(contenido)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def generar_codigo_qr(datos_reserva: dict) -> ContentFile:
    contenido = (
        f"HOTEL PACIFIC REEF\n"
        f"Reserva: #{datos_reserva['id']}\n"
        f"Cliente: {datos_reserva['cliente']}\n"
        f"Habitación: {datos_reserva['habitacion']}\n"
        f"Check-in: {datos_reserva['fecha_entrada']}\n"
        f"Check-out: {datos_reserva['fecha_salida']}\n"
        f"Garantía pagada: ${datos_reserva['garantia']}\n"
        f"Cód. transacción: {datos_reserva['codigo_transaccion']}"
    )
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(contenido)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f"qr_reserva_{datos_reserva['id']}.png")


def generar_codigo_transaccion():
    return f"TXN-{uuid.uuid4().hex[:10].upper()}"
