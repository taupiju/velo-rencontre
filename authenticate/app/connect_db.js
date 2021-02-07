const sqlite3 = require('sqlite3').verbose();

module.exports = {


    // Se connecter à la base
    connection_db: function (){
        return new sqlite3.Database('user_base.sqlite')
    },


    close_db: function (db){
        db.close()
    },


    execute_query: function (db, query, params){
        if (params)
            db.run(query, params, function(err) {
                if (err) {
                  return console.log(err.message);
                }
                // get the last insert id
                console.log(`A row has been inserted with rowid ${this.lastID} and ${this.username}`);
              });
        else
            db.run(query)
    },
    
    select_query: async function (db, query, params){
        if (params)
            return new Promise( (resolve,reject) => {
                db.all(query, params, function(err,rows){
                   if(err){return reject(err);}
                   resolve(rows);
                 });
                
            })
        else
            return new Promise( (resolve,reject) => {
                db.all(query, function(err,rows){
                   if(err){return reject(err);}
                   resolve(rows);
                 });
                
            })
    }

/*
    create_db: function (){
        try{
            conn = new sqlite3.Database('user_base.sqlite')
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE users("+
                    "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,"+
                    "username TEXT,"+
                    "password TEXT,"+
                    "email TEXT)"
            )
            conn.commit()
        }
        catch (e){
            if(e instanceof sqlite3.OperationalError)
                console.log('Erreur la table existe déjà')
            else{
                console.log("Erreur")
                conn.rollback()
                // raise e
            }
        }
        finally{
            conn.close()
        }
            
    }
    */

};
    