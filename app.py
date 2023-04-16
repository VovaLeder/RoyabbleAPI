import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique = False, nullable = False)
    password = db.Column('pass', db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f'{self.username}'

@app.post('/api/create_user')
def create_user():
    if request.is_json:
        data = request.get_json()
        request_username = data['username']
        request_password = data['password']

        user = UserModel.query.filter_by(username=request_username).first()
        if (user != None):
            return {'message': 'User already exists'}, 400

        new_user = UserModel(username=request_username, password=request_password)
        db.session.add(new_user)
        db.session.commit()
        return {'id': new_user.id, 'message': f'User {new_user.username} created.'}, 201
    else:
        return {'error': 'The request payload is not in JSON format'}, 400

@app.post('/api/get_user')
def get_user():

    if request.is_json:
        data = request.get_json()
        request_username = data['username']
        request_password = data['password']

        user = UserModel.query.filter_by(username=request_username).first()
        if (user == None):
            return {'message': 'User does not exist'}, 400
        if (user.password != request_password):
            return {'message': 'Wrong password'}, 400
        id = user.id
        return {'message': f'User {id} returned.'}