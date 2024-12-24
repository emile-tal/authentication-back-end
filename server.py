from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from app.queries.users import register_user, login_user, is_email_unique
from app.authentication import create_session, is_email_valid


load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user_id = login_user(email, password)
    if user_id is not None:
        session_cookie = create_session(user_id)
        response = make_response(jsonify({'message': "User logged in successfully"}), 200)
        response.set_cookie(session_cookie)
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
        user_id = register_user(email, password)
        session_cookie = create_session(user_id)
        response = make_response(jsonify({'message': "User regsitered successfully"}), 201)
        response.set_cookie(session_cookie)
    return response
  
