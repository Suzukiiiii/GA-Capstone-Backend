from flask import Flask, request, Response,jsonify
from database.db import initialize_db
from database.models import Session,Hand

app = Flask(__name__)

DEBUG = True
PORT = 8000

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/poker_hand_app'
}

initialize_db(app)

test_session = {
    "location": "Jacks Place",
    "start_money": 500,
    "end_money": 550
}

@app.route('/')
def hello():
    return "HelloGoodbye"

# All Sessions
@app.route('/Sessions')
def get_sessions():
    all_sessions = Session.objects().to_json()
    return Response(all_sessions,mimetype="application/jason",status=200)

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
    return jsonify(body)

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
@app.route('/Session/<id>/Hands')
def get_hands_by_session(id):
    hands = Hand.objects().get(session_id=id).to_json()
    return Response(hands,mimetype="application/jason",status=200)

@app.route('/Session/<id>/Hands',methods=['POST'])
def new_hand(id):
    return '',200
app.run(debug=DEBUG,port=PORT)