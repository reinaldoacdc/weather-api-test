import json
from forecast import Forecast
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/forecast/<city>')
def show_forecast(city):
    forecast = Forecast(city)
    return forecast.toJSON()

