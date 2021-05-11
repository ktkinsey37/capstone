from flask import Flask, render_template, request, jsonify
import random, requests

app = Flask(__name__)

open_weather_api_key = 'b0c9b96efc59a191000b51c7935e0b53'

38.083298, -109.569258

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("base.html")

@app.route("/special_locations/")

@app.route("/special_locations/add", methods=["GET", "POST"])

