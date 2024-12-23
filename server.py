from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from app.queries.users import registerUser, loginUser
from app.authentication import create_session


load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])
    

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if loginUser(email, password):
        session_cookie = create_session(email)
        response = make_response(jsonify({'message': "Successful log in"}))
        response.set_cookie(session_cookie)
    return response

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    registerUser(email, password)
    print("Register successful")
    return 'Success'
  
