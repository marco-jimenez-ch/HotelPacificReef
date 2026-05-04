from django.shortcuts import render, get_object_or_404
from .models import Habitacion
from apps.reservas.models import Reserva
from datetime import date
import urllib.request
import json


def obtener_clima():
    """Consume API externa Open-Meteo — sin API key requerida"""
    try:
        # Coordenadas de Viña del Mar (ubicación del Hotel Pacific Reef)
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

            # Convertir código WMO a descripción
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