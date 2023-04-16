from models.UserModel import UserModel
import bcrypt

def check_request_data(data):
    if (not('username' in data.keys()) or not('password' in data.keys())):
        return [1, ({'message': 'You have to have \'username\' and \'password\' fields in your request'}, 400)]

    request_username: str = data['username']
    request_password: str = data['password']

    if (request_username == '' or request_password == ''):
        return [1, ({'message': '\'username\' and \'password\' fields must have some value'}, 400)]

    if(not(is_all_alphanumberic_data(data))):
        return [1, ({'message': 'Only alphanumeric characters allowed ^_^'}, 400)]
    
    return [0, request_username, request_password]

def check_request_auth(data):
    if (not('auth_key' in data.keys())):
        return [1, ({'message': 'You have to have \'auth_key\' field in your request'}, 400)]

    request_auth_key: str = data['auth_key']

    if (request_auth_key == ''):
        return [1, ({'message': '\'auth_key\' field must have some value'}, 400)]

    if(not(is_all_alphanumberic_string(request_auth_key))):
        return [1, ({'message': 'Only alphanumeric characters allowed ^_^'}, 400)]

    user = UserModel.query.filter_by(auth_key=request_auth_key).first()
    if (user == None):
        return [1, ({'message': 'User does not exist'}, 400)]
    
    return [0, user]

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

                    "auth_key": "{user.auth_key}",

                    "games_played":   "{user.games_played}",
                    "games_won":      "{user.games_won}",
                    "earned_points":  "{user.earned_points}",
                    "spent_points":   "{user.spent_points}",
                    "words_composed": "{user.words_composed}",
                    "players_killed": "{user.players_killed}",
                }}
            }}
        '''
        
def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)