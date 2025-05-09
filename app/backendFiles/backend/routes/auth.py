from flask import Blueprint, request, jsonify
from models.user import User, db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = generate_password_hash(data['password'])  # Hash password
    user = User(name=data['name'], email=data['email'], password_hash=hashed_password)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password_hash, data['password']):  # Check hashed password
        token = create_access_token(identity=user.id)
        return jsonify({"token": token, "user_id": user.id}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401
