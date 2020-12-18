
from flask import Flask, request, Response,jsonify
from database.db import initialize_db
from database.models import Session,Hand,Card

session =  Session.objects.get(id='5fdc177e855dae9411e05c60')

print(session)
