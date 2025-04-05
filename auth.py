from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

users_db = {}

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users_db:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    users_db[username] = hashed_password
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username not in users_db or not check_password_hash(users_db[username], password):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)
