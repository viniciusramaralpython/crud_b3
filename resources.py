from flask import request, jsonify
from models import User, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


#Registrando o usuário
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201


#Executando o login
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


#Pegando os usuários utilizando JWT
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200


#Listando usuário por ID
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'username': user.username}), 200

#Atualizando o usuário
@jwt_required()
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)

    user.username = data.get('username', user.username)
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'User updated'}), 200

#Excluindo o usuário
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
