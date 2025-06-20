from django.shortcuts import render
from .weatherapi import get_city_weather


def index_index(request):
    data = get_city_weather(request.user)
    if not isinstance(data, dict):
        return render(request, 'main/index.html', {'weather_exception': data})
    return render(request, 'main/index.html', {'data': data})

