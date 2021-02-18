from flask import Flask
from flask import jsonify, request

import sqlite3

''' Se connecter à la base '''
def connection_db():
    return sqlite3.connect('profile_base.db')

def close_db(db):
    db.commit()
    db.close()

def execute_query(db, query, params=()):
    cursor = db.cursor()
    if params :
        cursor.execute(query, params)
    else :
        cursor.execute(query)
    
    return cursor

def create_db():
    try:
        conn = sqlite3.connect('profile_base.db')
        cursor = conn.cursor()
        cursor.execute("""
    CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT,
        age INTEGER,
        email TEXT,
        adresse TEXT,
        ville TEXT,
        resume TEXT
    )
    """)
        conn.commit()
    except sqlite3.OperationalError:
        print('Erreur la table existe déjà')
    except Exception as e:
        print("Erreur")
        conn.rollback()
        # raise e
    finally:
        conn.close()