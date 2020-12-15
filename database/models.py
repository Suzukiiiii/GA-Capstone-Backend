from .db import db
import datetime

class Card(db.EmbeddedDocument):
    rank = db.StringField(default = 'A')
    suit = db.StringField(defualt = 's')

class Hand(db.Document):
    session_id = db.StringField(required=True)
    hole_cards = db.ListField(db.EmbeddedDocumentField(Card),default = [])
    community_cards = db.ListField(db.StringField(), default = [])
    action = db.ListField(db.StringField(), default = [])
    starting_stack = db.IntField(default=0)
    ending_stack = db.IntField(default=0)
    
    def is_suited(self):
        return self.hole_cards[0].suit == self.hole_cards[1].suit
    
    def is_pocketpair(self):
        return self.hole_cards[0].rank == self.hole_cards[1].rank

    def is_connected(self):
        return True

class Session(db.Document):
    location = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.datetime.now())
    start_money = db.IntField(default=0)
    end_money = db.IntField(default=0)