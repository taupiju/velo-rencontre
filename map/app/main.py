import flask
from flask import jsonify, request

import folium, branca, json #Géolocalisation
import urllib.request   #Récuperer des données internet
import numpy as np 
import matplotlib.pyplot as plt
import webbrowser
import os
import requests
import urllib.parse
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def createMap(address1,address2):

    #address = 6%20Allée%20arnaud%20massy%20Bondoufle
    url = 'https://nominatim.openstreetmap.org/search/' + address1 +'?format=json'
    response = requests.get(url).json()
    lat1=float(response[0]["lat"])
    lon1=float(response[0]["lon"])

    url2 = 'https://nominatim.openstreetmap.org/search/' + address2 +'?format=json'
    response = requests.get(url2).json()
    lat2=float(response[0]["lat"])
    lon2=float(response[0]["lon"])

    #Création de la carte vierge
    map = folium.Map(location=((lat1+lat2)/2,(lon1+lon2)/2), tiles='OpenStreetMap', zoom_start=12)

    #Ajoute sur la carte des marker avec les données à afficher en cliquant dessus
    affichage="You (Damn Ugly)"
    affichage2="Your Crush"
    if(affichage!=""):
        folium.Marker(location = (lat1 , lon1),popup=affichage).add_to(map) 
        folium.Marker(location = (lat2 , lon2),popup=affichage2).add_to(map) 
    '''
    map.save(outfile='map.html')
    print('eveyrhing ok', file = sys.stderr)
    os.popen('map.html')
    '''

    return map

'''
# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]
'''
@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
'''
# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books/id', methods=['GET'])
def api_id():
    if "id" in request.args:
        return jsonify(books[int(request.args['id'])])
    else:
        return "Error: No id field provided. Please specify an id."
'''
@app.route('/api/v1/map', methods=['GET'])
def api_map():
    # exemple : http://127.0.0.1:5000/api/v1/map?address1=4%20Rue%20De%20La%20Paix%20Louveciennes&address2=6%20Allée%20arnaud%20massy%20Bondoufle
    if "address1" in request.args:
        address1 = request.args['address1']
    else:
        return "Request Lattitude and Longitude of targets"
    if "address2" in request.args:
        address2 = request.args['address2']
    else:
        return "Request Lattitude and Longitude of targets"
    map = createMap(address1,address2)
    return map._repr_html_()

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, port=5000)


