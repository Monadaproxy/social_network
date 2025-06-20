from social_network import settings
from django.core.cache import cache
import requests

def fetch_from_weatherapi(city):
    API_KEY = settings.OPENWEATHER_API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(url,params={
                'q': city,
                'appid': API_KEY,
                'units': 'metric',
                'lang': 'ru'
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе к API: {e}"

def get_city_weather(user):
    city = user.profile.city
    cache_key = f"weather_{city}"
    data = cache.get(cache_key)
    if not data:
        data = fetch_from_weatherapi(city)
        cache.set(cache_key, data, timeout=3600)
    return data