from flask import Flask, render_template, request, jsonify
import random, requests
from datetime import datetime, timedelta

app = Flask(__name__)

api_key = '2f8b1aca8f8d4e1c84c155556213105'
base_url = 'http://api.weatherapi.com/v1'

lat = 38.083298
long = -109.569258

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("base.html")

@app.route("/special_locations/")
def show_special_location():
    """Show a special location."""
    current = datetime.now()
    end = current - timedelta(hours=72)
    params = {'key':f'{api_key}', 'q':f'{lat}, {long}', 'dt':f'{end}', 'end_dt':f'{current}'}

    resp = requests.get(f'{base_url}/history.json', params=params)
    raise
    return str(resp.json())

@app.route("/special_locations/add", methods=["GET", "POST"])
def add_special_locations():
    return False