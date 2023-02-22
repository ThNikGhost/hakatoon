import requests
from django.shortcuts import render

def index(request):
    appid = '3fd71f50684a58f9c310b7a4e5df243f'
    city = 'London'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}'

    
    res = requests.get(url)
    print(res.text)
    return render(request, 'weather/index.html')
