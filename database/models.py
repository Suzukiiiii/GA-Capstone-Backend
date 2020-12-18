from .db import db
import datetime

class Card(db.EmbeddedDocument):
    rank = db.StringField(default = 'A')
    suit = db.StringField(defualt = 's')

class Hand(db.Document):
    session_id = db.StringField(required=True)
    hole_cards = db.ListField(db.EmbeddedDocumentField(Card),default = [])
    community_cards = db.ListField(db.EmbeddedDocumentField(Card), default = [])
    action = db.StringField(required=True)
    starting_stack = db.IntField(default=0)
    ending_stack = db.IntField(default=0)
    delta = db.IntField(default=0)
    is_suited = db.BooleanField(default = False)
    is_pocketpair = db.BooleanField(default = False)
    rank_gap = db.IntField(default = 0)
    

class Session(db.Document):
    location = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.datetime.now())
    start_money = db.IntField(default=0)
    end_money = db.IntField(default=0)
    delta = db.IntField(default=0)