from django.shortcuts import render
from .forms import TownForm
import requests

def transfer_temperature(T):
    "Перевод температуры из градусов Кельвина в градусы Цельсия"
    T = T - 273.15
    T = round(T, 2)
    return T

def transfer_pressure(P):
    "Перевод давления из гПа в мм рт. ст."
    P = P*100/133.3224
    P = round(P, 2)
    return P

def town_weather(request):
    "Получение информации о погоде в выбранном городе"

    if request.method == 'POST':                                        # В случае POST-запроса считываем название города из формы
        form = TownForm(request.POST)
        if form.is_valid():
            town_name = form.cleaned_data['town_name']
    else:                                                               # В противном случае город по умолчанию - Самара
        form = TownForm()
        town_name = 'Самара'

    country_code = 'RU'
    API_key = '5b65f99e785c9b22cca3eb29105347a9'
    lang = 'ru'

    # Запрос, в который мы передаём название города и код страны, а получаем в ответе широту и долготу
    url1 = f'http://api.openweathermap.org/geo/1.0/direct?q={town_name},{country_code}&limit=1&appid={API_key}'
    response1 = requests.get(url1)
    response1 = response1.json()                                        # Получаем ответ в формате JSON
    lat = response1[0]['lat']                                           # Широта
    lon = response1[0]['lon']                                           # Долгота

    # Запрос, в который мы передаём широту и долготу, а получаем в ответе информацию о погоде в данных координатах
    url2 = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&lang={lang}'
    response2 = requests.get(url2)
    response2 = response2.json()                                        # Получаем ответ в формате JSON
    
    state = response2['weather'][0]['description']                      # Общее погодное состояние
    temp = response2['main']['temp']                                    # Температура
    temp = transfer_temperature(temp)
    temp_feel = response2['main']['feels_like']                         # Температура по ощущениям
    temp_feel = transfer_temperature(temp_feel)
    wind = response2['wind']['speed']                                   # Скорость ветра
    pressure = response2['main']['pressure']                            # Давление
    pressure = transfer_pressure(pressure)
    
    # Данные, передаваемые в шаблон
    content = {'town_name': town_name, 'state': state, 'temp': temp, 'temp_feel': temp_feel, 'wind': wind, 
               'pressure': pressure, 'form': form}
    return render(request, 'town_weather.html', content)


