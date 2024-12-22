from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from app.queries.users import registerUser, loginUser

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])
    

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    loginUser(email, password)
    print("Login successful")
    return 'Success'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    registerUser(email, password)
    print("Register successful")
    return 'Success'
  
