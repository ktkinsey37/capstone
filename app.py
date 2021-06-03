from flask import Flask, render_template, request, jsonify
import random, requests
from datetime import datetime, timedelta

app = Flask(__name__)

api_key = '2f8b1aca8f8d4e1c84c155556213105'
base_url = 'http://api.weatherapi.com/v1'

lat =  35 # 38.083298
long =  -90 # -109.569258

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("base.html")

@app.route("/special_locations/")
def show_special_location():
    """Show a special location."""

    # Gets the current time, and 72 hours prior. Loads these, with coords and API key, into params.
    current = datetime.now()
    end = current - timedelta(hours=72)
    params = {'key':f'{api_key}', 'q':f'{lat}, {long}', 'dt':f'{end}', 'end_dt':f'{current}'}

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

    raise
    return str(resp.json())

@app.route("/special_locations/add", methods=["GET", "POST"])
def add_special_locations():
    return False