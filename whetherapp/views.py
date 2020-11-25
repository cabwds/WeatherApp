from django.shortcuts import render
import requests

apiKey = "128e920a702bfe9bd641ce398131c649"

# Create your views here.
def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=128e920a702bfe9bd641ce398131c649&units=metric"
    city = "New York"
    
    # get request, output r as response, parse as json dict
    r = requests.get(url.format(city)).json()
    #print(r)

    city_weather = { 
        'city' : city,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
    }
    #print(city_weather)

    # pass the dic within context and connect with the html
    context = {
        'city_weather' : city_weather,
    }
    return render(request, 'weather/weather.html', context) # will search within the templates folder in the app