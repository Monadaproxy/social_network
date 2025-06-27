from django.shortcuts import render, redirect
from .weatherapi import get_city_weather


def index_index(request):
    try:
        data = get_city_weather(request.user)
        if isinstance(data, dict):
            return render(request, 'main/index.html', {'data': data})
        return render(request, 'main/index.html', {'weather_exception': data})
    except AttributeError:
        return redirect('users:login')

