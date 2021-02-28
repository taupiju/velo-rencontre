from flask import Flask
from flask import jsonify, request, json
from flask_cors import CORS
import connect_db
import sqlite3
import jwt

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/")
def hello():
    connect_db.create_db()
    return "j'aime les BDD"

@app.route("/add", methods=['POST'])
def add_user():
    if request.method == 'POST':
        db = connect_db.connection_db()
        data = request.json
        params = (data['name'], data['age'], data['email'],data['adresse'],data['ville'],data['resume'])
        query = """
        INSERT INTO users(name, age, email, adresse, ville, resume) VALUES(?, ?, ?, ?, ?, ?)"""
        connect_db.execute_query(db, query, params)
        connect_db.close_db(db)

        response = app.response_class(
            response='user_created',
            status=200,
            mimetype='application/json'
        )

        return response

@app.route("/delete/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    if request.method == 'DELETE':
        db = connect_db.connection_db()
        query = """DELETE FROM users WHERE id=?"""
        result = connect_db.execute_query(db, query, (user_id))
        row_deleted = result.rowcount
        connect_db.close_db(db)

        if row_deleted == 0 :
            response = app.response_class(
                response=json.dumps(row_deleted),
                status=404,
             mimetype='application/json'
            )
        else : 
            response = app.response_class(
                response=json.dumps(row_deleted),
                status=203,
             mimetype='application/json'
            )

        return response 

@app.route("/update", methods=['POST'])
def update_user():
    token = request.json[1]

    if verifyToken(token):
        db = connect_db.connection_db()
        encoded_jwt = jwt.decode(token['token'], "Mon message secret", algorithms="HS256")
        user_id = encoded_jwt['sub']
        data = request.json[0]
        setter = ""
        params = ()

        try:
            if data["name"]:
                setter += " name= ? "
                params = (*params , str((data["name"])))
        except KeyError:
            pass

        try:
            if data["age"]:
                if setter != "":
                    setter += " , "
                setter += " age= ? "
                params = (*params , (data["age"]))
        except KeyError:
            pass

        try:
            if data["email"]:
                if setter != "":
                    setter += " , "
                setter += " email= ? "
                params = (*params , str((data["email"]))) 
        except KeyError:
            pass

        try:
            if data["adresse"]:
                if setter != "":
                    setter += " , "
                setter += " adresse= ? "
                params = (*params , str((data["adresse"]))) 
        except KeyError:
            pass

        try:
            if data["ville"]:
                if setter != "":
                    setter += " , "
                setter += " ville= ? "
                params = (*params , str((data["ville"]))) 
        except KeyError:
            pass

        try:
            if data["resume"]:
                if setter != "":
                    setter += " , "
                setter += " resume= ? "
                params = (*params , str((data["resume"]))) 
        except KeyError:
            pass
            

        params = (*params , int(user_id))
        query = """UPDATE users SET """ + setter + """WHERE id= ?"""
        
        response = app.response_class(
                response="no params",
                status=404,
                mimetype='application/json'
            )
        if params:
            result = connect_db.execute_query(db, query, params)
            user_updated = result.rowcount
            connect_db.close_db(db)

            response = app.response_class(
                response=json.dumps(user_updated),
                status=200,
                mimetype='application/json'
            )

        return response

@app.route("/get")
def get_users():
    db = connect_db.connection_db()
    query = """SELECT name, age, email, adresse, ville, resume FROM users"""
    result = connect_db.execute_query(db, query)
    users = result.fetchall()
    response = app.response_class(
            response=json.dumps(users),
            status=200,
            mimetype='application/json'
        )

    return response

@app.route("/get/<user_id>")
def get_user(user_id):
    db = connect_db.connection_db()
    query = """SELECT name, age, email FROM users WHERE id=?"""
    result = connect_db.execute_query(db, query, (user_id))
    user = result.fetchone()
    response = app.response_class(
            response=json.dumps(user),
            status=200,
            mimetype='application/json'
        )

    return response

@app.route("/get-other-users", methods=['POST'])
def get_other_users():
    db = connect_db.connection_db()
    data = request.json
    query = """SELECT name, age, email, adresse, ville FROM users WHERE email!=?"""
    result = connect_db.execute_query(db, query, (data["email"],))
    user = result.fetchall()
    response = app.response_class(
            response=json.dumps(user),
            status=200,
            mimetype='application/json'
        )

    return response

def verifyToken(token):
    try:
        jwt.decode(token['token'], "Mon message secret", algorithms="HS256")
        return True
    except:
        return False

@app.route("/getid",methods=['POST'])
def get_userid():
    token = request.json
    if verifyToken(token):
        db = connect_db.connection_db()
        encoded_jwt = jwt.decode(token['token'], "Mon message secret", algorithms="HS256")
        user_id = encoded_jwt['sub']
        query = """SELECT name, age, email, adresse, ville, resume FROM users WHERE id=?"""
        result = connect_db.execute_query(db, query, (str(user_id),))
        user = result.fetchone()
        response = app.response_class(
                response=json.dumps(user),
                status=200,
                mimetype='application/json'
            )

        return response
    else:
        return 'token expired!', 400
        

if __name__ == "__main__":
    # Only for debugging while developing
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True, port=5001)
