import os

from flask_wtf import FlaskForm
from flask import Flask, render_template, request, jsonify, flash, redirect, session, g
import random, requests
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, timedelta
from forms import SpecialLocationForm
from models import SpecialLocation, db, connect_db, DesertForecast

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///climbing-weather'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

api_key = '2f8b1aca8f8d4e1c84c155556213105'
base_url = 'http://api.weatherapi.com/v1'
bad_weather_words = ['sleet', 'Sleet' 'blizzard', 'Blizzard' 'drizzle', 'snow', 'Ice', 'ice', 'Thundery', 'rain', 'Drizzle', 'Snow']
sunny_weather_words = ['Sunny', 'Clear']
cloudy_weather_words = ['Partly cloudy', 'Cloudy', 'Overcast']

lat =  35 # 38.083298
long =  -90 # -109.569258

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("base.html")

@app.route("/special_locations/")
def show_special_location():
    """Show a special location."""
    special_locations = SpecialLocation.query.all()
    

    return render_template("special-location-list.html", special_locations=special_locations)

@app.route("/special_locations/add", methods=["GET", "POST"])
def add_special_locations():
        """
        """

        form = SpecialLocationForm()

        if form.validate_on_submit():
            
            special_location = SpecialLocation(name=form.name.data,
                                                location = form.location.data,
                                                latitude=form.latitude.data,
                                                longitude=form.longitude.data,
                                                image_url=form.image_url.data,
                                                description=form.description.data,
                                                is_desert=form.is_desert.data,
                                                is_snowy=form.is_snowy.data
                                                )
            db.session.add(special_location)
            db.session.commit()
                    
            return redirect("/")

        else:
            return render_template('special-location-add.html', form=form)


def check_for_precip(forecast):
    for day in forecast:
        for hour in day['hours']:
            if any(word in hour['condition'] for word in bad_weather_words):
                print('RAINY')
            else:
                print('NOT RAINY')

def check_for_sun_and_heat(forecast):
    for day in forecast:
        for hour in day['hours']:
            raise
    return True

def build_backcast():

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

    return app_forecast