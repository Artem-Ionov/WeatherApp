from django.shortcuts import render
from .forms import TownForm
import requests
from datetime import datetime, timedelta

API_key = '5b65f99e785c9b22cca3eb29105347a9'                            # Мой API-ключ для OpenWeatherMap
lang = 'ru'

def transfer_temperature(T):
    "Перевод температуры из градусов Кельвина в градусы Цельсия"
    T = T - 273.15
    T = round(T, 1)
    return T

def transfer_wind(wind_speed, wind_deg):
    "Округление скорости ветра и перевод его направления из градусов в словесную форму"
    wind_speed = round(wind_speed, 1)
    match wind_deg:
        case d if 0<=d<22.5 or d>=337.5:
            wind_deg = 'северный'
        case d if 22.5<=d<67.5:
            wind_deg = 'северо-восточный'
        case d if 67.5<=d<112.5:
            wind_deg = 'восточный'
        case d if 112.5<=d<157.5:
            wind_deg = 'юго-восточный'
        case d if 157.5<=d<202.5:
            wind_deg = 'южный'
        case d if 202.5<=d<247.5:
            wind_deg = 'юго-западный'
        case d if 247.5<=d<292.5:
            wind_deg = 'западный'
        case d if 292.5<=d<337.5:
            wind_deg = 'северо-западный'
    return wind_speed, wind_deg

def transfer_pressure(P):
    "Перевод давления из гПа в мм рт. ст."
    P = P*100/133.3224
    P = round(P, 1)
    return P

def get_coordinates(town_name):
    "Получение широты и долготы выбранного города"
    country_code = 'RU'
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={town_name},{country_code}&limit=1&appid={API_key}'
    response = requests.get(url)                                        # Делаем запрос по указанному url
    response = response.json()                                          # Получаем ответ в формате JSON
    lat = response[0]['lat']                                            # Широта
    lon = response[0]['lon']                                            # Долгота
    return lat, lon

def town_forecast(lat, lon):
    "Получение прогноза погоды для выбранного города"
    cnt = 16
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&lang={lang}&cnt={cnt}'
    response = requests.get(url)                                        # Делаем запрос по указанному url
    response = response.json()                                          # Получаем ответ в формате JSON
    Date = []; Time = []; Temp = []                                     # Инициализируем списки для сохранения данных
    delta_t = response['city']['timezone']                              # Получаем смещение в секундах относительно UTC для выбранного города
    delta_t = timedelta(seconds=delta_t)                                # Переводим смещение во временной формат
    for i in range(cnt):
        dt = response['list'][i]['dt']                                  # Получаем время в секундах с начала эпохи
        dt = datetime.utcfromtimestamp(dt)                              # Конвертируем в читаемый формат для UTC
        dt+=delta_t                                                     # Получаем дату и время в выбранном городе
        time = dt.strftime('%H:%M')                                     # Часы и минуты
        Time.append(time)
        date = dt.strftime('%d')                                        # День и месяц
        Date.append(date)
        temp = response['list'][i]['main']['temp']                      # Температура            
        temp = transfer_temperature(temp)
        Temp.append(temp)
    return Date, Time, Temp

def town_weather(request):
    "Получение информации о погоде в выбранном городе"
    
    if request.method == 'POST':                                        # В случае POST-запроса считываем название города из формы
        form = TownForm(request.POST)
        if form.is_valid():
            town_name = form.cleaned_data['town_name']
    else:                                                               # В противном случае город по умолчанию - Самара
        form = TownForm()
        town_name = 'Самара'

    lat, lon = get_coordinates(town_name)                               # Широта и долгота выбранного города

    # Запрос, в который мы передаём широту и долготу, а получаем в ответе информацию о погоде в данных координатах
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&lang={lang}'
    response = requests.get(url)                                        # Делаем запрос по указанному url
    response = response.json()                                          # Получаем ответ в формате JSON
    
    state = response['weather'][0]['description']                       # Общее погодное состояние
    temp = response['main']['temp']                                     # Температура
    temp = transfer_temperature(temp)
    temp_feel = response['main']['feels_like']                          # Температура по ощущениям
    temp_feel = transfer_temperature(temp_feel)
    wind_speed = response['wind']['speed']                              # Скорость ветра
    wind_deg = response['wind']['deg']                                  # Направление ветра
    wind_speed, wind_deg = transfer_wind(wind_speed, wind_deg)
    pressure = response['main']['pressure']                             # Давление
    pressure = transfer_pressure(pressure)
    
    Date, Time, Temp = town_forecast(lat, lon)                          # Прогноз погоды в выбранном городе

    # Данные, передаваемые в шаблон
    content = {'form': form, 'town_name': town_name, 'state': state, 'temp': temp, 'temp_feel': temp_feel, 'wind_speed': wind_speed, 
               'wind_deg': wind_deg, 'pressure': pressure, 'Date': Date, 'Time': Time, 'Temp': Temp}
    return render(request, 'town_weather.html', content)


