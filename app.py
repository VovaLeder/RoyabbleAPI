import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT, pass Text);"
)

INSERT_USER_RETURN_ID = "INSERT INTO users (username, pass) VALUES (%s, %s) RETURNING id;"

GET_USER = "SELECT * FROM users WHERE username = (%s)"

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")  # gets variables from environment
connection = psycopg2.connect(url)

@app.post("/api/create_user")
def create_user():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)

            cursor.execute(GET_USER, (username, ))
            if (cursor.fetchone() != None):
                return {"message": "User already exists"}, 400

            cursor.execute(INSERT_USER_RETURN_ID, (username, password, ))

            user_id = cursor.fetchone()[0]
    return {"id": user_id, "message": f"User {username} created."}, 201

@app.post("/api/get_user/")
def get_user():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER, (username,))
            obj = cursor.fetchone()

            if (obj == None):
                return {"message": "User does not exist"}, 400
            if (obj[2] != password):
                return {"message": "Wrong password"}, 400

            id = obj[0]
    return {"message": f"User {id} returned."}