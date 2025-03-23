from django.shortcuts import render
from django.http import HttpResponse
import requests

def transfer_temperature(T):
    T = T - 273.15
    T = round(T, 2)
    return T

def transfer_pressure(P):
    P = P*100/133.3224
    P = round(P, 2)
    return P

def town_weather(request):
    city_name = 'Samara'
    country_code = 'RU'
    API_key = '5b65f99e785c9b22cca3eb29105347a9'
    lang = 'ru'

    url1 = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=1&appid={API_key}'
    response1 = requests.get(url1)
    response1 = response1.json()
    lat = response1[0]['lat']                            # Широта
    lon = response1[0]['lon']                            # Долгота

    url2 = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&lang={lang}'
    response2 = requests.get(url2)
    response2 = response2.json()
    state = response2['weather'][0]['description']
    temp = response2['main']['temp']
    temp = transfer_temperature(temp)
    temp_feel = response2['main']['feels_like']
    temp_feel = transfer_temperature(temp_feel)
    wind = response2['wind']['speed']
    pressure = response2['main']['pressure']
    pressure = transfer_pressure(pressure)

    return HttpResponse(f'''
        Состояние погоды: {state}
        Температура сейчас: {temp} C
        Ощущается как: {temp_feel} C
        Скорость ветра: {wind} м/с
        Давление: {pressure} мм рт. ст.
    ''')

    print(response2)
    print(f'Состояние погоды: {state}')
    print(f'Температура сейчас: {temp} C')
    print(f'Ощущается как: {temp_feel} C')
    print(f'Скорость ветра: {wind} м/с')
    print(f'Давление: {pressure} мм рт. ст.')


