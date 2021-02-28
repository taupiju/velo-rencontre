'use strict';

const express = require('express');
const expressJwt = require('express-jwt');
//const config = require('./config.json');
const jwt2 = require('jsonwebtoken');
const connect_db = require('./connect_db')
const sqlite3 = require('sqlite3').verbose();
const router = express.Router();

require('rootpath')();

const cors = require('cors');
const bodyParser = require('body-parser');

// Constants
const PORT = 5004;
const HOST = '0.0.0.0';

// App
const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(cors());

// use JWT auth to secure the api
app.use(jwt());

//global error handler
app.use(errorHandler);
!
// api routes
//app.use('/users', require('./users/users.controller'));
app.use('/authenticate',authenticate);
app.use('/verifyAuthenticate', verifyAuthenticate);
app.use('/signup', signup);
app.use('/updateAccount', updateAccount);
app.use('/deleteAccount', deleteAccount);

app.use((req, res, next) => { 

    res.setHeader('Access-Control-Allow-Origin', '*'); 

    res.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content, Accept, Content-Type, Authorization'); 

    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS'); 

    next(); 

});

// routes
router.post('/authenticate', authenticate);
router.post('/verifyAuthenticate', verifyAuthenticate);
router.post('/signup', signup);
router.put('/updateAccount', updateAccount);
router.put('/deleteAccount', deleteAccount);

// users hardcoded for simplicity, store in a db for production applications

var users = "";
async function refreshUsers(){
    const promiseUsers = getUsers();
    promiseUsers.then((v_users) => {
        users = v_users;
        //console.log(users)
    });
}

refreshUsers()


function errorHandler(err, req, res, next) {
    if (typeof (err) === 'string') {
        // custom application error
        return res.status(400).json({ message: err });
    }

    if (err.name === 'UnauthorizedError') {
        // jwt authentication error
        return res.status(401).json({ message: 'Invalid Token' });
    }

    // default to 500 server error
    return res.status(500).json({ message: err.message });
}

function authenticate(req, res, next) {
        authenticate2(req.body,res)
        .then(
            token => res.json(token)
        )
        .catch(next);
}

function verifyAuthenticate(req, res, next) {
        verifyAuthenticate2(req.body)
        .then(
            
            user => res.json(user)
        )
        .catch(next);
}

function signup(req, res, next) {
        signup2(req.body)
        .then(user => res.json(user))
        .catch(next);
}

function updateAccount(req, res, next) {
        updateAccount2(req.body)
        .then(res.json("Account was update"))
        .catch(next);
}

function deleteAccount(req, res, next) {
        deleteAccount2(req.body)
        .then(res.json("Account was deleted"))
        .catch(next);
}

async function authenticate2({ username, password },res) {
    
    refreshUsers();
    
    const user = users.find(u => u.username === username && u.password === password);
    
    if (!user){
        throw 'Username or password is incorrect';
    }

    // create a jwt token that is valid for 7 days
    const token = jwt2.sign({ sub: user.id }, "Mon message secret", { expiresIn: '1d' });
    
    return {
        user,
        token
    };
}

async function verifyAuthenticate2(reqbody) {
    const usertoken = jwt2.verify(reqbody.token,"Mon message secret");
    
    console.log(usertoken);
    const userid = usertoken.sub;
    const user = users.find(u => u.id === userid);
    let bol = JSON.stringify("true");
    
    if (!user){
        bol = JSON.stringify("false");
        return bol;
    } 

    return bol;
}

async function signup2(reqbody) {
    let addedUser = reqbody;
    
    var db = connect_db.connection_db();
    
    var query = "INSERT INTO users (username, password, email) VALUES(?, ?, ?)"
    
    var params = [addedUser['username'], addedUser['password'], addedUser['email']]
    
    connect_db.execute_query(db,query,params)

    refreshUsers();

    const user = users[users.length-1]
    
    connect_db.close_db(db);
    
    return {user};
}

async function updateAccount2(reqbody) {
    const userid = reqbody.id;
    let index = users.find(u => u.id === userid);
    index = index.id;
    if(reqbody.password)
        users[index-1]['password'] = reqbody.password;
    if(reqbody.email)
        users[index-1]['email'] = reqbody.email;
    
    const user = users[index-1].username
    
    return {user};
}

async function deleteAccount2(reqbody) {
    const userid = reqbody.id;
    let index = users.find(u => u.id === userid);
    index = index.id;
    const user = users[index-1].username;
    users = users.splice(index-2,1);
    
    return {user};
}

async function getUsers(){
    var db = connect_db.connection_db();
    
    var query = "SELECT id, username, password, email FROM users"
    
    var result = await connect_db.select_query(db,query)
    
    connect_db.close_db(db);
    
    return result;
}


function jwt() {
    const { secret } = {"secret": "Mon message secret"};
    return expressJwt({ secret, algorithms: ['HS256'] }).unless({
        path: [
            // public routes that don't require authentication
            '/authenticate',
            '/',
            '/signup',
            '/verifyAuthenticate'
        ]
    });
}

app.get('/', (req, res) => {
  res.send('Hello World ');
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);