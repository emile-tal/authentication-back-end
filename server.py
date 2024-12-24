from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from app.queries.users import registerUser, loginUser
from app.authentication import create_session


load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])

# TO DO validate email/password (characters/length) frontend backend
    

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user_id = loginUser(email, password)
    if user_id is not None:
        session_cookie = create_session(user_id)
        response = make_response(jsonify({'message': "Successful log in"}))
        response.set_cookie(session_cookie)
        return response
    response = make_response(jsonify({'message': 'Username or password incorrect'}))
    return response

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user_id = registerUser(email, password)
    session_cookie = create_session(user_id)
    response = make_response(jsonify({'message': "Successful log in"}))
    response.set_cookie(session_cookie)
    return response
  
