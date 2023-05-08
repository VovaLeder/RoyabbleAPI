import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_migrate import Migrate
from models.UserModel import UserModel
from models import db
from utils.utils import check_request_data, check_request_auth, return_success_user, check_password, get_hashed_password

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db.init_app(app)
migrate = Migrate(app, db)

@app.post('/api/create_user')
def create_user():
    if request.is_json:
        data = request.get_json()

        check_result = check_request_data(data)
        if check_result[0] == 1:
            return check_result[1]
        request_username = check_result[1]
        request_password = check_result[2]

        if (len(request_password) < 4):
            return {'message': '\'password\' field must be at least 4 symbols length'}, 400

        user = UserModel.query.filter_by(username=request_username).first()
        if (user != None):
            return {'message': 'User already exists'}, 400

        new_user = UserModel(username=request_username, password=get_hashed_password(request_password))
        db.session.add(new_user)
        db.session.commit()
        return return_success_user(new_user), 201
    else:
        return {'message': 'The request payload is not in JSON format'}, 400

@app.post('/api/get_user')
def get_user():
    if request.is_json:
        data = request.get_json()
        
        check_result = check_request_data(data)
        if check_result[0] == 1:
            return check_result[1]
        request_username = check_result[1]
        request_password = check_result[2]

        user = UserModel.query.filter_by(username=request_username).first()
        if (user == None):
            return {'message': 'User does not exist'}, 400
        if (not(check_password(request_password, user.password))):
            return {'message': 'Wrong password'}, 400

        return return_success_user(user), 200
    else:
        return {'message': 'The request payload is not in JSON format'}, 400
    
@app.post('/api/get_user_by_auth')
def get_user_by_auth():
    if request.is_json:
        data = request.get_json()
        
        check_result = check_request_auth(data)
        if check_result[0] == 1:
            return check_result[1]
        user = check_result[1]

        return return_success_user(user), 200
    else:
        return {'message': 'The request payload is not in JSON format'}, 400
    
@app.put('/api/change_user')
def change_user():
    if request.is_json:
        data = request.get_json()
        
        check_result = check_request_auth(data)
        if check_result[0] == 1:
            return check_result[1]
        user = check_result[1]
        
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
    
if __name__ == '__main__':
    app.run(debug=True)