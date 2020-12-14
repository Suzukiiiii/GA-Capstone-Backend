
from flask import Flask, request, Response,jsonify
from database.db import initialize_db
from database.models import Session,Hand,Card

body = {"location":"somewhere"}
new_Session = Session(**body)

print(new_Session.location)