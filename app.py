import os

from capstone_api_keys import google_api_key, api_key
from weather_helper import Location, desert_weather_assessment, build_backcast, find_avg_and_highest_wind, find_avg_and_total_precip, find_avg_and_highest_temp, check_for_precip, check_for_sun, check_for_clouds
from flask_wtf import FlaskForm
from flask import Flask, render_template, request, jsonify, flash, redirect, session, g
import random, requests
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, timedelta
from forms import SpecialLocationForm, BackcastEditForm, UserAddForm, EditUserProfileForm, LoginForm
from sqlalchemy.exc import IntegrityError
from models import SpecialLocation, db, connect_db, Backcast, User

app = Flask(__name__)

CURR_USER_KEY = "curr_user"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///climbing-weather'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

google_api = google_api_key
api_key = api_key
base_url = 'http://api.weatherapi.com/v1'


########################### USER ROUTES ############################
@app.before_request
def add_user_to_g():
    """If user is in session, retrieve them"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    flash("Successfully logged out!")
    session.pop(CURR_USER_KEY)
    return redirect('/login', code=302)


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template('home.html')

########################### SPECIAL LOCATION ROUTES ############################
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

    app_backcast.assessment = desert_weather_assessment()

    db.session.add(app_backcast)
    db.session.commit()

    return render_template('backcast.html', special_location=special_location, backcast=full_backcast, app_backcast=app_backcast)

@app.route('/special_locations/<special_location_id>/backcasts')
def special_location_backcasts_show(special_location_id):
    """Show a special location and its details."""

    special_location = SpecialLocation.query.get_or_404(special_location_id)

    backcasts = Backcast.query.filter_by(location_id=special_location_id).all()

    return render_template('special-location-backcast-list.html', special_location=special_location, backcasts=backcasts)

########################### BACKCAST ROUTES ############################
@app.route('/backcast/<backcast_id>', methods=["GET", "POST"])
def show_full_or_edit_backcast(backcast_id):

        form = BackcastEditForm()

        backcast = Backcast.query.get_or_404(backcast_id)

        if form.validate_on_submit():

            backcast.user_report = form.user_report.data
  
            db.session.add(backcast)
            db.session.commit()
            return render_template("backcast.html", backcast=backcast)

        else:
            return render_template('backcast-edit.html', form=form)

@app.route('/backcast/new_backcast', methods=["POST"])
def create_custom_location_backcast():

    location = Location(request.form['latbox'], request.form['lngbox'], False, False)

    full_backcast = build_backcast(api_key, base_url, location)
    avg_wind, high_wind = find_avg_and_highest_wind(full_backcast)
    avg_temp, high_temp = find_avg_and_highest_temp(full_backcast)
    avg_precip, total_precip = find_avg_and_total_precip(full_backcast)
    precip_count = check_for_precip(full_backcast)
    cloud_count = check_for_clouds(full_backcast)
    sun_count = check_for_sun(full_backcast)

    app_backcast = Backcast(
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

    return render_template('backcast.html', backcast=full_backcast, app_backcast=app_backcast, location=location)