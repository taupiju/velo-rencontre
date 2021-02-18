import flask
from flask import jsonify, request
from flask_cors import CORS


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
cors = CORS(app, resources={r"*": {"origins": "*"}})

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
    map = folium.Map(location=((lat1+lat2)/2,(lon1+lon2)/2), tiles='OpenStreetMap')
    map.fit_bounds([[lat1,lon1],[lat2,lon2]])
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


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/map')
def api_map():
    '''
    db = connect_db.connection_db()
    query = """SELECT email FROM users"""
    result = connect_db.execute_query(db, query)
    users = result.fetchall()
    response = app.response_class(
            response=json.dumps(users),
            status=200,
            mimetype='application/json'
        )
    print(response)
    '''
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

