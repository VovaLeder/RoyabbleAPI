from models import db
import secrets

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column('pass', db.String(), nullable = False)

    auth_key = db.Column(db.String(), unique = True, nullable = False)

    games_played = db.Column(db.Integer(), default=0, server_default='0', nullable=False)
    games_won = db.Column(db.Integer(), default=0, server_default='0', nullable=False)

    earned_points = db.Column(db.Integer(), default=0, server_default='0', nullable=False)
    spent_points = db.Column(db.Integer(), default=0, server_default='0', nullable=False)
    words_composed = db.Column(db.Integer(), default=0, server_default='0', nullable=False)
    players_killed = db.Column(db.Integer(), default=0, server_default='0', nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.auth_key = secrets.token_hex(32)

    def __repr__(self) -> str:
        return f'{self.username}'