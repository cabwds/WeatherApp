from django.shortcuts import render, get_object_or_404, redirect
import requests
from .models import City
from .forms import CityForm

apiKey = "128e920a702bfe9bd641ce398131c649"

# Create your views here.
def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=128e920a702bfe9bd641ce398131c649&units=metric"
    # city = "Singapore"
    
    err_msg = ''
    delete_msg = ''
    message = ''
    message_class = ''

    # to differentiate POST and GET
    if request.method == 'POST':
        # print(request.POST)
        if "_add_button" in request.POST : 
            form = CityForm(request.POST)
            if form.is_valid():
                new_city = form.cleaned_data['name'].capitalize()
                existing_city_count = City.objects.filter(name=new_city).count()
                # to check for duplicated cities
                if existing_city_count == 0:
                    # here need to check if the input city name is actually existing
                    r = requests.get(url.format(new_city)).json()
                    # usually if request successful, 'cod' = 200
                    # if request failed, 'cod' = 404
                    if r['cod'] == 200 :
                        # after validation then save
                        form.save()
                    else:
                        err_msg = "{} does not exist in the world!".format(new_city)
                else:
                    err_msg =  "City already exists in the database!"
        # elif "_delete_button" in request.POST :
        #     del_city_id = request.POST['_delete_button']
        #     #print(del_item) 
        #     del_item = get_object_or_404(City, pk=del_city_id)
        #     del_item.delete()
        #     delete_msg = "{} is being deleted from Database successfully!".format(del_item.name)

        if err_msg:
            message = err_msg
            message_class = "is-danger"
        elif delete_msg: 
            message = delete_msg
            message_class = 'is-success'
        else:
            message = "{} added successfully!".format(new_city)
            message_class = "is-success"

    
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
        'form' : form,
        'message' : message,
        'message_class' : message_class,
    }
    return render(request, 'weather/weather.html', context) # will search within the templates folder in the app



def delete_city(request, city_name):
    del_item = get_object_or_404(City, name=city_name)
    del_item.delete()
    return redirect('home')