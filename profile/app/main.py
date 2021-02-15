from flask import Flask
from flask import jsonify, request, json
import connect_db
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello():
    connect_db.create_db()
    return "j'aime les BDD"

@app.route("/add", methods=['POST'])
def add_user():
    if request.method == 'POST':
        db = connect_db.connection_db()
        data = request.json
        params = (data['name'], data['age'], data['email'])
        query = """
        INSERT INTO users(name, age, email) VALUES(?, ?, ?)"""
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

@app.route("/update/<user_id>", methods=['POST'])
def update_user(user_id):
    if request.method == 'POST':
        db = connect_db.connection_db()
        data = request.json
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
            

        params = (*params , int(user_id))
        query = """UPDATE users SET """ + setter + """WHERE id= ?"""
        
        response = app.response_class(
                response="no params",
                status=404,
                mimetype='application/json'
            )
        print(params)
        print(query)
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
    query = """SELECT name, age, email FROM users"""
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

if __name__ == "__main__":
    # Only for debugging while developing
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True, port=5001)
