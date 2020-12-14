from .db import db
import datetime

class Hand(db.Document):
    session_id = db.StringField(required=True)
    hole_cards = db.ListField(db.StringField(),required=True)
    community_cards = db.ListField(db.StringField())
    action = db.ListField(db.StringField())
    starting_stack = db.IntField(default=0)
    ending_stack = db.IntField(default=0)

class Session(db.Document):
    location = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.datetime.now())
    start_money = db.IntField(default=0)
    end_money = db.IntField(default=0)
    hands = EmbeddedDocumentListField('Hand')
