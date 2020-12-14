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

@app.route('/Sessions',methods=['GET'])
def get_sessions():
    return "All of the sessions"

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

app.run()