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
                "velocidad_viento": weather.get("windsp

cat > apps/habitaciones/views.py << 'ENDOFFILE'
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
                "velocidad_viento": weather.get("windsp
python -m py_compile apps/habitaciones/views.py && echo "OK"
git add apps/habitaciones/views.py
git commit -m "fix: corregir sintaxis en habitaciones/views.py"
git push origin main
