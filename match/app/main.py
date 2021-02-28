from flask import Flask
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

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/",methods=['POST'])
def match_by_city():

    print("JE SUIS IC LALALAL")
    print(request)
    print(request.json)
    data = request.json
    print(data)
    json_data = {
        "email" : data["email"]
    }
    
    profiles = requests.post("http://profile:5001/get-other-users", json = json_data)

    coord_user_url = "https://nominatim.openstreetmap.org/search/" + data["city"] + "?format=json"
    response = requests.get(coord_user_url).json()
    lat_user = float(response[0]["lat"])
    lon_user = float(response[0]["lon"])

    departement_user_url = "https://nominatim.openstreetmap.org/reverse.php?lat=" + str(lat_user) + "&lon=" + str(lon_user) + "&zoom=8&format=jsonv2"
    response_departement = requests.get(departement_user_url).json()
    departement_user = response_departement["address"]["county"]

    match_profiles = []
    profiles_data = json.loads(profiles.content)

    for other_user in profiles_data:

        city = other_user[4]
    
        other_user_url = "https://nominatim.openstreetmap.org/search.php?city=" + city + "&county=" + departement_user + "&polygon_geojson=1&format=jsonv2"
        #other_user_url = "https://nominatim.openstreetmap.org/search/" + city + "?format=json"
        response = requests.get(other_user_url).json()
        print(response)
        if response :
            match_profiles.append(other_user)
    
    if not match_profiles :
        return 'no content', 204

    response = app.response_class(
                response=json.dumps(match_profiles),
                status=200,
                mimetype='application/json'
            )
    
    return response


if __name__ == "__main__":
    # Only for debugging while developing
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True, port=5005)