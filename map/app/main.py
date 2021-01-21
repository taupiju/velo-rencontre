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
    return "j'aime les fleurs"

if __name__ == "__main__":
    # Only for debugging while developing
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True, port=5000)