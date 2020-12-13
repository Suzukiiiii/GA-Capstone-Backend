from flask import Flask, request, Response,jsonify
from database.db import initialize_db
import database.models

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/27017'
}

initialize_db(app)

session = {
    "location": "Jacks Place",
    "start_money": 500,
    "end_money": 550
}

@app.route('/')
def hello():
    return "HelloGoodbye"

app.run()