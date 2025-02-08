import requests
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

@api_view(['GET'])
def get_weather(request, city_code):
    cached_data = cache.get(city_code)
    if cached_data:
        return Response(cached_data)
    try:
        api_key = settings.WEATHER_API_KEY
        # url=f"http://api.openweathermap.org/data/2.5/weather?id={city_code}&applid={api_key}"
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_code}&units=metric&appid={api_key}'
        response = requests.get(url)
        data = response.json()
        cache.set(city_code, data, timeout=60*60)
        return Response(data)
    except requests.exceptions.RequestException as e:
        return Response({"error: ": str(e)}, status=500)