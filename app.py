from flask import Flask, request, Response,jsonify
from database.db import initialize_db
from database.models import Session,Hand,Card
from flask_cors import CORS
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
CORS(app)

# HELPER METHODS

def is_suited(card1,card2):
        return card1.suit == card2.suit
    
def is_pocketpair(card1,card2):
        return card1.rank == card2.rank

def calc_rank_gap(card1,card2):
        diff = 0

        rank_map = {
            "2":2,
            "3":3,
            "4":4,
            "5":5,
            "6":6,
            "7":7,
            "8":8,
            "9":9,
            "10":10,
            "T":10,
            "J":11,
            "Q":12,
            "K":13,
            "A":14
        }

        # A can be 1 or 14, so calc the smaller absolute difference of 1-card or 14- card
        # Other wise calc abs value of card1-card2
        if(card1.rank == "A"):
            diff = min(abs(1-rank_map[card2.rank]),abs(14-rank_map[card2.rank]))
        elif(card2.rank == "A"):
            diff = min(abs(rank_map[card1.rank]-1),abs(rank_map[card1.rank]-14))
        else:
            diff = abs(rank_map[card1.rank]-rank_map[card2.rank])
        
        # subtract 1 from diff
        # that is the gap (number of spaces between ranks) between two cards
        return diff - 1

#ROUTES

@app.route('/')
def hello():
    return "HelloGoodbye"

@app.route('/search')
def data():
    # here we want to get the value of user (i.e. ?user=some-value)
    return ''

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

# Index Hands in single session
@app.route('/Sessions/<id>/Hands',methods=['GET'])
def get_hands_in_session(id):
    session_hands = Hand.objects(session_id__in=[id]).to_json()

    return Response(session_hands,mimetype="application/json",status=200)
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

    hand.is_suited = is_suited(hole_card1,hole_card2)
    hand.is_pocketpair = is_pocketpair(hole_card1,hole_card2)
    hand.rank_gap = calc_rank_gap(hole_card1,hole_card2)

    hand.save()
    return {'id':str(hand.id)}, 200

# Delete Hand
@app.route('/Hands/<id>',methods=['DELETE'])
def delete_hand(id):
    Hand.objects.get(id=id).delete()
    return 'Hand deleted ',200

app.run(debug=DEBUG,port=PORT)