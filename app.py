from flask import Flask, request, Response,jsonify
from database.db import initialize_db
from database.models import Session,Hand,Card

# from flask_mongoengine import MongoEngine

# db = MongoEngine()

# def initialize_db(app):
#     db.init_app(app)
#     print('connected to db',app)

app = Flask(__name__)

DEBUG = True
PORT = 5000

app.config['MONGODB_SETTINGS'] = {
    'host': 'localhost',
    'port': 27017,
    'connect': True,
    'db': 'poker_hand_app'
}

# app.config['MONGODB_CONNECT'] = False

initialize_db(app)
#db.init_app(app)

#ROUTES

@app.route('/')
def hello():
    return "HelloGoodbye"

# All Sessions
@app.route('/Sessions')
def get_sessions():
    all_sessions = Session.objects().to_json()
    return Response(all_sessions,mimetype="application/json",status=200)

# Get Session by id
@app.route('/Sessions/<id>')
def get_session_by_id(id):
    session = Session.objects.get(id=id).to_json()
    return Response(session,mimetype="application/json",status=200)

# Add new Session
@app.route('/Sessions',methods=['POST'])
def add_session():
    body = request.get_json()
    session = Session(**body).save()
    id = session.id
    return {'id':str(id)}, 200
    #return jsonify(body)

# Update Session
@app.route('/Sessions/<id>',methods=['PUT'])
def update_session(id):
    body = request.get_json()
    Session.objects.get(id=id).update(**body)
    return 'Session '+id+' updated',200

# Delete Session
@app.route('/Sessions/<id>',methods=['DELETE'])
def delete_session(id):
    Session.objects.get(id=id).delete()
    return 'Session deleted ',200

# Get all Hands by Session id
# @app.route('/Session/<id>/Hands')
# def get_hands_by_session(id):
#     hands = Hand.objects().get(session_id=id).to_json()
#     return Response(hands,mimetype="application/jason",status=200)

@app.route('/Session/<id>/Hands',methods=['POST'])
def new_hand(id):
    body = request.get_json()
    hand=Hand(**body).save()
    return 'hand posted',200


app.run(debug=DEBUG,port=PORT)

#http://localhost:8000/Sessions/5fd6f791855daeabe7b9f61f/Hands

# get all hands in 

# JSON for testing hands POST
{

    "hole_cards": [{"rank":"A","suit":"h"},{"rank":"A","suit":"s"}]

}