from flask import Flask, request, Response,jsonify
from database.db import initialize_db
from database.models import Session

app = Flask(__name__)

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

@app.route('/Sessions')
def get_sessions():
    all_sessions = Session.objects().to_json()
    return Response(all_sessions,mimetype="application/jason",status=200)

@app.route('/Sessions/<id>')
def get_session_by_id(id):
    session = Session.objects.get(id=id).to_json()
    return Response(session,mimetype="application/json",status=200)

@app.route('/Sessions',methods=['POST'])
def add_session():
    body = request.get_json()
    session = Session(**body).save()
    id = session.id
    return {'id':str(id)}, 200
    return jsonify(body)

@app.route('/Sessions/<id>',methods=['PUT'])
def update_session(id):
    body = request.get_json()
    Session.objects.get(id=id).update(**body)
    return 'Session '+id+' updated',200

@app.route('/Sessions/<id>',methods=['DELETE'])
def delete_session(id):
    Session.objects.get(id=id).delete()
    return 'Session deleted ',200

app.run()