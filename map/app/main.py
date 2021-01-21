from flask import Flask
from flask import jsonify, request

import folium, branca, json #Géolocalisation
import urllib.request   #Récuperer des données internet
import numpy as np 
import matplotlib.pyplot as plt
import webbrowser
import os
import requests
import urllib.parse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World from Flask"

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)