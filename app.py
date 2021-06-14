import os

from weather_helper import build_backcast, find_avg_and_highest_wind, find_avg_and_total_precip, find_avg_and_highest_temp, check_for_precip, check_for_sun, check_for_clouds
from flask_wtf import FlaskForm
from flask import Flask, render_template, request, jsonify, flash, redirect, session, g
import random, requests
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, timedelta
from forms import SpecialLocationForm
from models import SpecialLocation, db, connect_db, Backcast

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///climbing-weather'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

google_api = 'AIzaSyANrWPh7m9NNCAX9usYfXtrb1mS7RDPkaU'
api_key = '2f8b1aca8f8d4e1c84c155556213105'
base_url = 'http://api.weatherapi.com/v1'

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("base.html")

@app.route("/special_locations/")
def show_special_location():
    """Show a list of special locations."""
    special_locations = SpecialLocation.query.all()

    return render_template("special-location-list.html", special_locations=special_locations)

@app.route("/special_locations/add", methods=["GET", "POST"])
def add_special_locations():
        """Form for adding special locations. Handles showing and processing the form."""

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

@app.route('/special_locations/<special_location_id>')
def special_location_show(special_location_id):
    """Show a special location and its details."""

    special_location = SpecialLocation.query.get_or_404(special_location_id)

    return render_template('special-location-view.html', special_location=special_location)

@app.route('/special_locations/<special_location_id>/backcast')
def create_and_show_full_backcast(special_location_id):
    """Build and display a full backcast, saves the backcast parameters to rebuild it"""

    special_location = SpecialLocation.query.get_or_404(special_location_id)
    full_backcast = build_backcast(api_key, base_url, special_location)
    avg_wind, high_wind = find_avg_and_highest_wind(full_backcast)
    avg_temp, high_temp = find_avg_and_highest_temp(full_backcast)
    avg_precip, total_precip = find_avg_and_total_precip(full_backcast)
    precip_count = check_for_precip(full_backcast)
    cloud_count = check_for_clouds(full_backcast)
    sun_count = check_for_sun(full_backcast)

    app_backcast = Backcast(
                    location_id=special_location_id,
                    sun_count=sun_count,
                    cloud_count=cloud_count,
                    precip_count=precip_count,
                    total_precip=total_precip,
                    avg_precip=avg_precip,
                    avg_temp=avg_temp,
                    avg_wind=avg_wind,
                    high_temp=high_temp,
                    high_wind=high_wind
    )

    app_backcast.assessment = app_backcast.desert_weather_assessment()

    db.session.add(app_backcast)
    db.session.commit()

    return render_template('special-location-backcast.html', special_location=special_location, backcast=full_backcast, app_backcast=app_backcast)

@app.route('/special_locations/<special_location_id>/backcasts')
def special_location_backcasts_show(special_location_id):
    """Show a special location and its details."""

    special_location = SpecialLocation.query.get_or_404(special_location_id)

    backcasts = Backcast.query.filter_by(location_id=special_location_id).all()

    return render_template('special-location-backcast-list.html', special_location=special_location, backcasts=backcasts)

@app.route('/backcast/<backcast_id>', methods=["GET", "POST"])
def show_full_or_edit_backcast(backcast_id):

    backcast = Backcast.query.get_or_404(backcast_id)

    return str(backcast.assessment)