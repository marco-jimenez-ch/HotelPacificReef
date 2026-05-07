from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from .models import Habitacion
from apps.reservas.models import Reserva
from datetime import date, datetime
import urllib.request
import json


def obtener_clima():
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
                0: ("Despejado", "Soleado"),
                1: ("Mayormente despejado", "Casi despejado"),
                2: ("Parcialmente nublado", "Parcial"),
                3: ("Nublado", "Nublado"),
                45: ("Neblina", "Neblina"),
                51: ("Llovizna leve", "Llovizna"),
                61: ("Lluvia leve", "Lluvia"),
                80: ("Chubascos", "Chubascos"),
                95: ("Tormenta", "Tormenta"),
            }
            desc, icono = descripciones.get(codigo, ("Variable", "?"))
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
            "icono": "?",
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
    if request.method == "POST" and not request.user.is_authenticated:
        return redirect("/accounts/login/?next=/reservas/nueva/" + str(pk) + "/")
    return render(request, "habitaciones/detalle.html", {
        "habitacion": habitacion,
        "hoy": date.today().isoformat(),
    })


@login_required
@require_GET
def api_habitaciones_lista(request):
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
    return JsonResponse({"status": "ok", "total": len(data), "habitaciones": data})


@login_required
@require_GET
def api_habitacion_detalle(request, pk):
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
    return JsonResponse({"status": "ok", "habitacion": data})


@login_required
@require_GET
def api_disponibilidad(request):
    habitacion_id = request.GET.get("habitacion_id")
    fecha_entrada_str = request.GET.get("fecha_entrada")
    fecha_salida_str = request.GET.get("fecha_salida")

    if not all([habitacion_id, fecha_entrada_str, fecha_salida_str]):
        return JsonResponse({"status": "error", "mensaje": "Parametros requeridos"}, status=400)

    try:
        fecha_entrada = datetime.strptime(fecha_entrada_str, "%Y-%m-%d").date()
        fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"status": "error", "mensaje": "Formato invalido. Use YYYY-MM-DD"}, status=400)

    if fecha_salida <= fecha_entrada:
        return JsonResponse({"status": "error", "mensaje": "Fecha salida debe ser posterior"}, status=400)

    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)

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
        "habitacion_id": habitacion.id,
        "noches": noches,
        "disponible": disponible,
        "precio_por_noche": int(habitacion.precio_por_noche),
        "costo_total": int(habitacion.precio_por_noche) * noches if disponible else None,
        "garantia_30_porciento": int(habitacion.precio_por_noche * noches * 3 / 10) if disponible else None,
        "mensaje": "Disponible" if disponible else "No disponible",
    })
