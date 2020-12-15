from flask import Flask, request, Response,jsonify
from database.db import initialize_db
from database.models import Session,Hand,Card

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

    # get session with matching id
    session = Session.objects.get(id=id).to_json()

    # get all hands in the session
    session_hands = Hand.objects(session_id__in=[id])


    print('Session Hands: ',session_hands)
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

# Show hand
@app.route('/Hands/<id>')
def show_hand(id):
    print('Hand SHOW')
    # get hand with matching id
    hand = Hand.objects.get(id=id).to_json()
    #return 'zzz'
    return Response(hand,mimetype="application/json",status=200)

def create_card(rank,suit):
    card = Card()
    card.rank = rank
    card.suit = suit

    return card

# Add a new hand
@app.route('/Sessions/<id>/Hands',methods=['POST'])
def new_hand(id):
    print('Hand POST')
    body = request.get_json()

    hand_json = {"session_id":id}

    hole_card1 = create_card(body['card1_rank'],body['card1_suit'])
    hole_card2 = create_card(body['card2_rank'],body['card2_suit'])

    hand=Hand(**hand_json)

    hand.hole_cards.append(hole_card1)
    hand.hole_cards.append(hole_card2)

    hand.save()
    return {'id':str(hand.id)}, 200

app.run(debug=DEBUG,port=PORT)