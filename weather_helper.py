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
    round(avg_temp, 2)
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
    round(avg_precip, 2)
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
    round(avg_wind, 2)
    return (avg_wind, high_wind)

def build_backcast(api_key, base_url, location):

    # Gets the current time, and 72 hours prior. Loads these, with coords and API key, into params.
    current = datetime.now()

    if location.is_desert:
        end = current - timedelta(days=3)
        print("HITTING DESERT ROUTE")
    elif location.is_snowy:
        end = current - timedelta(days=7) #need to upgrade to get farther back
    else:
        end = current - timedelta(days=2)
        print("HITTING NOT DESERT ROUTE")
    
    params = {'key':f'{api_key}', 'q':f'{location.latitude},{location.longitude}', 'dt':f'{end}', 'end_dt':f'{current}'}

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

class LocationBuilder:
    def __init__(self, latitude, longitude, is_desert, is_snowy):
        self.latitude = latitude
        self.longitude = longitude
        self.is_desert = is_desert
        self.is_snowy = is_snowy


def desert_weather_assessment(backcast):
    """Assesses the weather to determine if a sandstone area should be climbed on.
    """
    
    if backcast.total_precip == 0:
        return 'No precipitation in the recent past, climb on.'
    if backcast.total_precip > 2:
        return "There's been over two inches(~5cm) of precip in the past 72 hrs, you probably shouldn't climb."
    if backcast.sun_count > 30 and backcast.high_temp > 40:
        return f"It's rained {backcast.total_precip} recently here, but also been sunny for {backcast.sun_count} of the last 72 hours and has reached {backcast.high_temp}F. Use your discretion."
    if backcast.precip_count > 30 and backcast.avg_temp < 50:
        return f"It's rained {backcast.total_precip} recently here, over {backcast.precip_count} of the last 72 hours, with an average temp of {backcast.avg_temp}F. Use your discretion and please stay safe."
    return f"It's rained {backcast.total_precip} recently here, over {backcast.precip_count} of the last 72 hours, with an average temp of {backcast.avg_temp}F. "

def mountain_weather_assessment(backcast):
    """Assesses the weather to determine if an alpine area should be climbed on.
    """
    
    if backcast.total_precip < 6:
        return 'Less than 6 inches of precipitation in the past 7 days, climb on.'
    if backcast.total_precip > 36:
        return f"There's been {backcast.total_precip} of precip in the past 7 days, you probably shouldn't climb."
    if backcast.sun_count > 72 and backcast.high_temp > 40:
        return f"It's precipitated {backcast.total_precip} inches recently here, but also been sunny for {backcast.sun_count} hours and reached {backcast.high_temp} degrees F. Use your discretion."
    if backcast.precip_count > 30 and backcast.avg_temp <= 40:
        return f"It's precipitated {backcast.total_precip} inches recently here, over {backcast.precip_count} hours out of the last 7 days, with an average temp of {backcast.avg_temp}F. Use your discretion and please stay safe."
    return f"Not sure how to assess this information."

# def location_env_determiner(location, form):
#         if form.env.data is "alp":
#             location.is_snowy = True, location.is_desert = False
#         elif form.env.data is "sand":
#             location.is_snowy = False, location.is_desert = True
#         elif form.env.data is "none":
#             location.is_snowy = False, location.is_desert = False
#         return location