from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])
    

@app.route('/login', methods=['POST'])
def login():
    print("Login successful")

@app.route('/register', methods=['POST'])
def register():
    print("Login successful")
  
