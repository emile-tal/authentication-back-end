import os
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from app.queries.users import register_user, login_user, is_email_unique, get_user_name
from app.authentication import create_session, validate_session, is_email_valid


load_dotenv()

app = Flask(__name__)
CORS(app, origins=[os.environ['FRONT_END_URL']])

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user_id = login_user(email, password)
    if user_id is not None:
        session_cookie = create_session(user_id)
        response = make_response(jsonify({'message': "User logged in successfully"}), 200)
        response.set_cookie('session_cookie', session_cookie, domain='localhost:5173', samesite='None', secure=False, httponly=True, max_age=3600)
    else:
        response = make_response(jsonify({'message': 'Username or password incorrect'}), 401)
    return response

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if len(password) < 8:
        response = make_response(jsonify({'message': 'Password length too short'}), 400)
    elif is_email_valid(email) is None:
        response = make_response(jsonify({'message': 'Email is invalid'}), 400)
    elif not is_email_unique(email):
        response = make_response(jsonify({'message': 'Email is already registered'}), 400)
    else:
        user_id = register_user(email, password, data['first_name'], data['last_name'])
        session_cookie = create_session(user_id)
        response = make_response(jsonify({'message': "User regsitered successfully"}), 201)
        response.set_cookie('session_cookie', session_cookie, samesite='None', secure=False)
    return response
  
@app.route('/user-details', methods=['GET'])
def get_user():
    session_cookie = request.cookies['session_cookie']
    print(f'session cookie: {session_cookie}')
    if session_cookie is None:
        response = make_response(jsonify({'message': 'User is not logged in'}), 401)
    else:
        user_id = validate_session(session_cookie)
        if user_id is None:
            response = make_response(jsonify({'message': 'Session is not valid'}), 401)
        else:
            user_name = get_user_name(user_id)
            response = make_response(jsonify({'name': user_name}), 200)
            response.set_cookie(session_cookie)
    return response
