import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column('pass', db.String(), nullable = False)

    games_played = db.Column(db.Integer(), default=0, server_default='0', nullable=False)
    games_won = db.Column(db.Integer(), default=0, server_default='0', nullable=False)

    earned_points = db.Column(db.Integer(), default=0, server_default='0', nullable=False)
    spent_points = db.Column(db.Integer(), default=0, server_default='0', nullable=False)
    words_composed = db.Column(db.Integer(), default=0, server_default='0', nullable=False)
    players_killed = db.Column(db.Integer(), default=0, server_default='0', nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f'{self.username}'

@app.post('/api/create_user')
def create_user():
    if request.is_json:
        data = request.get_json()

        if (not('username' in data.keys()) or not('password' in data.keys())):
            return {'message': 'You have to have \'username\' and \'password\' fields in your request'}, 400

        request_username: str = data['username']
        request_password: str = data['password']



        if (request_username == '' or request_password == ''):
            return {'message': '\'username\' and \'password\' fields must have some value'}, 400

        if (len(request_password) < 4):
            return {'message': '\'password\' field must be at least 4 symbols length'}, 400
    
        if(not(is_all_alphanumberic_data(data))):
            return {'message': 'Only alphanumeric characters allowed ^_^image.png'}, 400



        user = UserModel.query.filter_by(username=request_username).first()
        if (user != None):
            return {'message': 'User already exists'}, 400

        new_user = UserModel(username=request_username, password=request_password)
        db.session.add(new_user)
        db.session.commit()
        return return_success_user(new_user), 201
    else:
        return {'message': 'The request payload is not in JSON format'}, 400

@app.post('/api/get_user')
def get_user():
    if request.is_json:
        data = request.get_json()
        
        if (not('username' in data.keys()) or not('password' in data.keys())):
            return {'message': 'You have to have \'username\' and \'password\' fields in your request'}, 400

        request_username: str = data['username']
        request_password: str = data['password']

        if (request_username == '' or request_password == ''):
            return {'message': '\'username\' and \'password\' fields must have some value'}, 400

        if (len(request_password) < 4):
            return {'message': '\'password\' field must be at least 4 symbols length'}, 400
    
        if(not(is_all_alphanumberic_data(data))):
            return {'message': 'Only alphanumeric characters allowed ^_^image.png'}, 400



        user = UserModel.query.filter_by(username=request_username).first()
        if (user == None):
            return {'message': 'User does not exist'}, 400
        if (user.password != request_password):
            return {'message': 'Wrong password'}, 400

        return return_success_user(user), 200
    else:
        return {'message': 'The request payload is not in JSON format'}, 400
    
@app.put('/api/change_user')
def change_user():
    if request.is_json:
        data = request.get_json()

        if (not('username' in data.keys()) or not('password' in data.keys())):
            return {'message': 'You have to have \'username\' and \'password\' fields in your request'}, 400

        request_username: str = data['username']
        request_password: str = data['password']

        if (request_username == '' or request_password == ''):
            return {'message': '\'username\' and \'password\' fields must have some value'}, 400

        if (len(request_password) < 4):
            return {'message': '\'password\' field must be at least 4 symbols length'}, 400
    
        if(not(is_all_alphanumberic_data(data))):
            return {'message': 'Only alphanumeric characters allowed ^_^image.png'}, 400


        user = UserModel.query.filter_by(username=request_username).first()
        if (user == None):
            return {'message': 'User does not exist'}, 400
        if (user.password != request_password):
            return {'message': 'Wrong password'}, 400
        
        request_games_played = data['games_played'] if 'games_played' in data.keys() else 0
        request_games_won = data['games_won'] if 'games_won' in data.keys() else 0
        request_earned_points = data['earned_points'] if 'earned_points' in data.keys() else 0
        request_spent_points = data['spent_points'] if 'spent_points' in data.keys() else 0
        request_words_composed = data['words_composed'] if 'words_composed' in data.keys() else 0
        request_players_killed = data['players_killed'] if 'players_killed' in data.keys() else 0

        user.games_played += request_games_played
        user.games_won += request_games_won
        user.earned_points += request_earned_points
        user.spent_points += request_spent_points
        user.words_composed += request_words_composed
        user.players_killed += request_players_killed

        db.session.add(user)
        db.session.commit()

        return return_success_user(user), 201
    else:
        return {'message': 'The request payload is not in JSON format'}, 400
    
def is_all_alphanumberic_string(string: str):
    return all(c.isalnum() for c in string)

def is_all_alphanumberic_data(data: dict):
    if (not(is_all_alphanumberic_string(data['username']))):
        return False
    if (not(is_all_alphanumberic_string(data['password']))):
        return False
    return True

def return_success_user(user: UserModel):
    return f'''
            {{
                "message": "Success",

                "user": {{
                    "username": "{user.username}",
                    "password": "{user.password}",

                    "games_played":   "{user.games_played}",
                    "games_won":      "{user.games_won}",
                    "earned_points":  "{user.earned_points}",
                    "spent_points":   "{user.spent_points}",
                    "words_composed": "{user.words_composed}",
                    "players_killed": "{user.players_killed}",
                }}
            }}
        '''
        