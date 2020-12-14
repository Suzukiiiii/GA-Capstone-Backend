from .db import db
import datetime

class Card():
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit

class Hand(db.EmbeddedDocument):
    session_id = db.StringField(required=True)
    #hole_cards = db.ListField(Card,required = True)
    hole_cards = db.ListField(db.StringField(),required=True)
    community_cards = db.ListField(db.StringField(), default = [])
    action = db.ListField(db.StringField(), default = [])
    starting_stack = db.IntField(default=0)
    ending_stack = db.IntField(default=0)

    def is_suited(self):
        return True
    
    def is_connected():
        return True
class Session(db.Document):
    location = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.datetime.now())
    start_money = db.IntField(default=0)
    end_money = db.IntField(default=0)
    hands = db.ListField(db.EmbeddedDocumentField(Hand))
