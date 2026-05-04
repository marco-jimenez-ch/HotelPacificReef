from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Habitacion
from apps.reservas.models import Reserva
from datetime import date, datetime
import urllib.request
import json


def obtener_clima():
    """Consume API externa Open-Meteo — sin API key requerida"""
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=-33.0245"
            "&longitude=-71.5518"
            "&current_weather=true"
            "&timezone=America%2FSantiago"
        )
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            weather = data.get("current_weather", {})
            codigo = weather.get("weathercode", 0)
            descripciones = {
                0: ("Despejado", "☀️"),
                1: ("Mayormente despejado", "🌤️"),
                2: ("Parcialmente nublado", "⛅"),
                3: ("Nublado", "☁️"),
                45: ("Neblina", "🌫️"),
                48: ("Neblina con escarcha", "🌫️"),
                51: ("Llovizna leve", "🌦️"),
                53: ("Llovizna moderada", "🌦️"),
                61: ("Lluvia leve", "🌧️"),
                63: ("Lluvia moderada", "🌧️"),
                65: ("Lluvia intensa", "🌧️"),
                71: ("Nieve leve", "❄️"),
                80: ("Chubascos", "🌦️"),
                95: ("Tormenta", "⛈️"),
            }
            desc, icono = descripciones.get(codigo, ("Variable", "🌡️"))
            return {
                "temperatura": weather.get("temperature", "--"),
                "velocidad_viento": weather.get("windspeed", "--"),
                "descripcion": desc,
                "icono": icono,
                "disponible": True,
            }
    except Exception:
        return {
            "temperatura": "--",
            "velocidad_viento": "--",
            "descripcion": "No disponible",
            "icono": "🌡️",
            "disponible": False,
        }


def home(request):
    habitaciones_destacadas = Habitacion.objects.filter(disponible=True)[:3]
    clima = obtener_clima()
    return render(request, "home.html", {
        "habitaciones": habitaciones_destacadas,
        "clima": clima,
    })


def lista_habitaciones(request):
    tipo_filtro = request.GET.get("tipo", "")
    fecha_entrada = request.GET.get("fecha_entrada", "")
    fecha_salida = request.GET.get("fecha_salida", "")
    habitaciones = Habitacion.objects.filter(disponible=True)
    if tipo_filtro:
        habitaciones = habitaciones.filter(tipo=tipo_filtro)
    return render(request, "habitaciones/lista.html", {
        "habitaciones": habitaciones,
        "tipo_filtro": tipo_filtro,
        "fecha_entrada": fecha_entrada,
        "fecha_salida": fecha_salida,
    })


def detalle_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    return render(request, "habitaciones/detalle.html", {
        "habitacion": habitacion,
        "hoy": date.today().isoformat(),
    })


# ─── API REST INTERNA ─────────────────────────────────────────────────────────

@require_GET
def api_habitaciones_lista(request):
    """
    API interna — RF-04
    GET /api/habitaciones/
    Retorna lista de habitaciones disponibles en formato JSON.
    Permite filtro por tipo: /api/habitaciones/?tipo=suite
    """
    tipo = request.GET.get("tipo", "")
    habitaciones = Habitacion.objects.filter(disponible=True)
    if tipo:
        habitaciones = habitaciones.filter(tipo=tipo)

    data = [
        {
            "id": h.id,
            "numero": h.numero,
            "tipo": h.tipo,
            "tipo_display": h.get_tipo_display(),
            "capacidad": h.capacidad,
            "precio_por_noche": int(h.precio_por_noche),
            "descripcion": h.descripcion,
            "disponible": h.disponible,
        }
        for h in habitaciones
    ]

    return JsonResponse({
        "status": "ok",
        "fuente": "Hotel Pacific Reef API v1.0",
        "total": len(data),
        "habitaciones": data,
    })


@require_GET
def api_habitacion_detalle(request, pk):
    """
    API interna — RF-04
    GET /api/habitaciones/<id>/
    Retorna detalle de una habitación específica en JSON.
    """
    habitacion = get_object_or_404(Habitacion, pk=pk)

    data = {
        "id": habitacion.id,
        "numero": habitacion.numero,
        "tipo": habitacion.tipo,
        "tipo_display": habitacion.get_tipo_display(),
        "capacidad": habitacion.capacidad,
        "precio_por_noche": int(habitacion.precio_por_noche),
        "descripcion": habitacion.descripcion,
        "disponible": habitacion.disponible,
    }

    return JsonResponse({
        "status": "ok",
        "fuente": "Hotel Pacific Reef API v1.0",
        "habitacion": data,
    })


@require_GET
def api_disponibilidad(request):
    """
    API interna — RF-03
    GET /api/disponibilidad/?habitacion_id=1&fecha_entrada=2026-06-01&fecha_salida=2026-06-05
    Verifica si una habitación está disponible para un rango de fechas.
    """
    habitacion_id = request.GET.get("habitacion_id")
    fecha_entrada_str = request.GET.get("fecha_entrada")
    fecha_salida_str = request.GET.get("fecha_salida")

    # Validar parámetros requeridos
    if not all([habitacion_id, fecha_entrada_str, fecha_salida_str]):
        return JsonResponse({
            "status": "error",
            "mensaje": "Parámetros requeridos: habitacion_id, fecha_entrada, fecha_salida",
        }, status=400)

    # Validar formato de fechas
    try:
        fecha_entrada = datetime.strptime(fecha_entrada_str, "%Y-%m-%d").date()
        fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({
            "status": "error",
            "mensaje": "Formato de fecha inválido. Use YYYY-MM-DD",
        }, status=400)

    if fecha_salida <= fecha_entrada:
        return JsonResponse({
            "status": "error",
            "mensaje": "La fecha de salida debe ser posterior a la fecha de entrada",
        }, status=400)

    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)

    # Verificar si existe reserva confirmada o pendiente que se cruce con las fechas
    reservas_cruzadas = Reserva.objects.filter(
        habitacion=habitacion,
        estado__in=["confirmada", "pendiente"],
        fecha_entrada__lt=fecha_salida,
        fecha_salida__gt=fecha_entrada,
    )

    disponible = not reservas_cruzadas.exists()
    noches = (fecha_salida - fecha_entrada).days

    return JsonResponse({
        "status": "ok",
        "fuente": "Hotel Pacific Reef API v1.0",
        "habitacion_id": habitacion.id,
        "habitacion_numero": habitacion.numero,
        "habitacion_tipo": habitacion.get_tipo_display(),
        "fecha_entrada": fecha_entrada_str,
        "fecha_salida": fecha_salida_str,
        "noches": noches,
        "disponible": disponible,
        "precio_por_noche": int(habitacion.precio_por_noche),
        "costo_total": int(habitacion.precio_por_noche) * noches if disponible else None,
        "garantia_30_porciento": int(habitacion.precio_por_noche * noches * 3 / 10) if disponible else None,
        "mensaje": "Habitación disponible para las fechas solicitadas" if disponible
                   else "Habitación no disponible para las fechas solicitadas",
    })