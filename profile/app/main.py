from flask import Flask
from flask import jsonify, request

import json #Géolocalisation
import sqlite3
import numpy as np 
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route("/")
def hello():
    db = sqlite3.connect('profile_base.db')
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT,
        age INTERGER
    )
    """)
    db.commit()
    db.close()
    return "j'aime les fleurs"

@app.route("/add")
def add_user():
    if "user_name" in request.args:
        db = sqlite3.connect('profile_base.db')
        cursor = db.cursor()
        cursor.execute("""
        INSERT INTO users(name, age) VALUES(?, ?)""", (request.args['user_name'],22))
        db.commit()
        db.close()
    return "User added"

@app.route("/get")
def get_user():
    db = sqlite3.connect('profile_base.db')
    cursor = db.cursor()
    cursor.execute("""SELECT name, age FROM users""")
    user1 = cursor.fetchone()

    return "User : " + str(user1)

if __name__ == "__main__":
    # Only for debugging while developing
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True, port=5001)
