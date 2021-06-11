from datetime import datetime, timedelta
import requests
from flask import Flask, render_template, request, jsonify, flash, redirect, session, g

bad_weather_words = ['sleet', 'Sleet' 'blizzard', 'Blizzard' 'drizzle', 'snow', 'Ice', 'ice', 'Thundery', 'rain', 'Drizzle', 'Snow']
sunny_weather_words = ['Sunny', 'Clear']
cloudy_weather_words = ['Partly cloudy', 'Cloudy', 'Overcast']

def check_for_precip(forecast):
    precip_count = 0
    for day in forecast:
        for hour in day['hours']:
            if any(word in hour['condition'] for word in bad_weather_words):
               precip_count += 0
    return precip_count

def check_for_sun(forecast):
    sunny_count = 0
    for day in forecast:
        for hour in day['hours']:
            if any(word in hour['condition'] for word in sunny_weather_words):
                sunny_count += 1
    return sunny_count

def check_for_clouds(forecast):
    cloudy_count = 0
    for day in forecast:
        for hour in day['hours']:
            if any(word in hour['condition'] for word in cloudy_weather_words):
                cloudy_count += 1
    return cloudy_count

def find_avg_and_highest_temp(forecast):
    hour_count = 0
    total_temp = 0
    high_temp = 0
    for day in forecast:
        for hour in day['hours']:
            hour_count += 1
            total_temp += hour['temp']
            if high_temp > hour['temp']:
                high_temp = hour['temp']
    avg_temp = total_temp / hour_count
    return (avg_temp, high_temp)

def find_avg_and_total_precip(forecast):
    hour_count = 0
    total_precip = 0
    high_precip = 0
    for day in forecast:
        for hour in day['hours']:
            hour_count += 1
            total_precip += hour['precip']
            if high_precip > hour['precip']:
                high_precip = hour['precip']
    avg_precip = total_precip / hour_count
    return (avg_precip, total_precip)

def find_avg_and_highest_wind(forecast):
    hour_count = 0
    total_wind = 0
    high_wind = 0
    for day in forecast:
        for hour in day['hours']:
            hour_count += 1
            total_wind += hour['wind']
            if high_wind > hour['wind']:
                high_wind = hour['wind']
    avg_wind = total_wind / hour_count
    return (avg_wind, high_wind)

def build_backcast(api_key, base_url, location):

    # Gets the current time, and 72 hours prior. Loads these, with coords and API key, into params.
    current = datetime.now()
    if location.is_desert:
        end = current - timedelta(hours=72)
    if location.is_snowy:
        end = current - timedelta(days=30)
    
    params = {'key':f'{api_key}', 'q':f'{location.latitude}, {location.longitude}', 'dt':f'{end}', 'end_dt':f'{current}'}

    # Gets the forecast request and names it more manageably.
    resp = requests.get(f'{base_url}/history.json', params=params)
    forecast = resp.json()['forecast']['forecastday']

    # Builds the app-side forecast from the full forecast (makes it more manageable at this point)
    app_forecast = []
    for day in forecast:
        app_day = {'date': day['date'], 'hours': []}
        for hour in day['hour']:
            app_hour = {'time': hour['time'], 'precip': hour['precip_in'], 'condition': hour['condition']['text'], 'temp': hour['temp_f'], 'wind': hour['wind_mph']}
            app_day['hours'].append(app_hour)
        app_forecast.append(app_day)

    return app_forecast
