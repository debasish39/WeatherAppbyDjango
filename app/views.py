from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime
from decouple import config

API_KEY = config('OPENWEATHER_API_KEY')

def home(request):
    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Bhubaneswar'

    # Step 1: Get coordinates
    geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}'
    geo_response = requests.get(geo_url).json()

    if not geo_response:
        return HttpResponse("Invalid city name")

    lat = geo_response[0]['lat']
    lon = geo_response[0]['lon']

    # Step 2: Get weather data
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
    PARAMS = {'units': 'metric'}
    data = requests.get(weather_url, params=PARAMS).json()

    # Extract values
    description = data['weather'][0]['description']
    icon = data['weather'][0]['icon']
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    day = datetime.date.today()

    return render(request, 'app/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'humidity': humidity,
        'day': day,
        'city': city
    })
