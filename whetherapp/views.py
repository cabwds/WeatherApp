from django.shortcuts import render, get_object_or_404
import requests
from .models import City
from .forms import CityForm

apiKey = "128e920a702bfe9bd641ce398131c649"

# Create your views here.
def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=128e920a702bfe9bd641ce398131c649&units=metric"
    # city = "Singapore"
    
    # to differentiate POST and GET
    if request.method == 'POST':
        print(request.POST)
        if "_add_button" in request.POST : 
            form = CityForm(request.POST)
            form.save()
        elif "_delete_button" in request.POST :
            del_city_id = request.POST['_delete_button']
            #print(del_item) 
            del_item = get_object_or_404(City, pk=del_city_id)
            del_item.delete()

    
    form = CityForm()

    # retrieve data from City model 
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        # get request, output r as response, parse as json dict
        r = requests.get(url.format(city)).json()
        #print(r)

        city_weather = { 
            'city_id' : city.pk,
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        #print(city_weather)

        # for each city in the database, loop over and append to the obj list
        weather_data.append(city_weather)

    # pass the array dic within context and connect with the html
    context = {
        'weather_data' : weather_data,
        'form' : form
    }
    return render(request, 'weather/weather.html', context) # will search within the templates folder in the app