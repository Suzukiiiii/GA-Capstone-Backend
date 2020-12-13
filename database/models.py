from .db import db
import datetime

class Session(db.Document):
    location = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.datetime.now())
    start_money = db.IntField(default=0)
    end_money = db.IntField(default=0)