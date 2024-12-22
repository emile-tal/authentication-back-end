from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from app.queries.users import registerUser

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])
    

@app.route('/login', methods=['POST'])
def login():
    print("Login successful")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    print(email, password)
    registerUser(email, password)
    print("Register successful")
    return 'Success'
  
