"""
Este script le habla a una API PÚBLICA real, que nosotros NO construimos:
Open-Meteo (https://open-meteo.com), un servicio gratuito de clima que
no pide registrarte ni pedir una API key. Es la opción más simple para
ver cómo se siente consumir una API que no es la tuya.

Nota: en la mayoría de APIs reales sí necesitarías una API key
(una especie de contraseña que te identifica). Aquí no, para simplificar,
pero ya vamos a hablar de eso después.
"""

import requests

# Coordenadas de Ciudad de Panamá (latitud, longitud).
# Si quieres el clima de otro lugar, solo cambia estos dos números.
LATITUD = 8.9824
LONGITUD = -79.5199


def obtener_clima_actual(lat: float, lon: float) -> dict:
    """Le pregunta a Open-Meteo el clima actual de una ubicación."""
    respuesta = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,  # queremos el clima de AHORA, no el pronóstico
        },
    )
    respuesta.raise_for_status()
    return respuesta.json()


if __name__ == "__main__":
    datos = obtener_clima_actual(LATITUD, LONGITUD)

    print("Respuesta completa de la API:")
    print(datos)

    clima = datos["current_weather"]
    print("\n--- Clima actual en Ciudad de Panamá ---")
    print(f"Temperatura: {clima['temperature']}°C")
    print(f"Viento: {clima['windspeed']} km/h")
    print(f"Hora del dato: {clima['time']}")
