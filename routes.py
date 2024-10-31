from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal
from auth import token_required, role_required  # Импортируем декораторы
import jwt
import datetime

bp = Blueprint('routes', __name__)
bcrypt = Bcrypt()


# Эндпоинт для регистрации
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    role = data.get('role', 'user')

    new_user = User(username=data['username'], email=data['email'], password=hashed_password, role=role)

    db: Session = SessionLocal()  # создаем сессию
    existing_user = db.query(User).filter_by(username=data['username']).first()
    if existing_user:
        db.close()
        return jsonify({'message': 'Username already exists'}), 400

    db.add(new_user)
    db.commit()
    db.close()

    return jsonify({'message': 'User registered successfully', 'role': role}), 201


# Эндпоинт для получения токена
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db: Session = SessionLocal()
    user = db.query(User).filter_by(username=data['username']).first()

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        db.close()
        return jsonify({'message': 'Invalid username or password'}), 400

    token = jwt.encode({'sub': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       'your_secret_key', algorithm="HS256")
    db.close()
    return jsonify({'access_token': token, 'token_type': 'bearer'})


# Защищенный эндпоинт для получения профиля
@bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({'username': current_user.username, 'email': current_user.email, 'role': current_user.role})


# Защищенный эндпоинт для обновления профиля
@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.get_json()
    db: Session = SessionLocal()
    db_user = db.query(User).filter_by(username=current_user.username).first()
    db_user.email = data.get('email', db_user.email)
    db.commit()
    db.close()
    return jsonify({'message': 'Profile updated successfully'})


# Защищенный эндпоинт для удаления профиля
@bp.route('/profile', methods=['DELETE'])
@token_required
def delete_profile(current_user):
    db: Session = SessionLocal()
    db_user = db.query(User).filter_by(username=current_user.username).first()
    db.delete(db_user)
    db.commit()
    db.close()
    return jsonify({'message': 'User deleted successfully'})


# Эндпоинт для администраторов для создания новых пользователей
@bp.route('/admin/register', methods=['POST'])
@token_required
@role_required('admin')
def admin_register(current_user):
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password,
                    role=data.get('role', 'user'))

    db: Session = SessionLocal()
    db.add(new_user)
    db.commit()
    db.close()
    return jsonify({'message': 'User registered successfully by admin'}), 201


# Эндпоинт для тестирования
@bp.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'Test successful'})
