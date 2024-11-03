from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal
from auth import token_required, role_required
import jwt
import datetime

bp = Blueprint('routes', __name__)
bcrypt = Bcrypt()

# Эндпоинт для регистрации
@bp.route('/register', methods=['POST'])
def register():
    """
    Регистрация пользователя
    ---
    tags:
      - User Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Имя пользователя
            email:
              type: string
              description: Email пользователя
            password:
              type: string
              description: Пароль пользователя
            role:
              type: string
              description: Роль пользователя (по умолчанию \"user\")
    responses:
      201:
        description: Пользователь успешно зарегистрирован
      400:
        description: Имя пользователя уже существует
    """
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    role = data.get('role', 'user')

    new_user = User(username=data['username'], email=data['email'], password=hashed_password, role=role)

    db: Session = SessionLocal()
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
    """
    Получение токена доступа
    ---
    tags:
      - User Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Имя пользователя
            password:
              type: string
              description: Пароль пользователя
    responses:
      200:
        description: Успешный вход в систему
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: Токен доступа
            token_type:
              type: string
              description: Тип токена
      400:
        description: Неверное имя пользователя или пароль
    """
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
    """
    Получение профиля пользователя
    ---
    tags:
      - User Management
    security:
      - Bearer: []
    responses:
      200:
        description: Профиль пользователя
        schema:
          type: object
          properties:
            username:
              type: string
            email:
              type: string
            role:
              type: string
    """
    return jsonify({'username': current_user.username, 'email': current_user.email, 'role': current_user.role})

# Защищенный эндпоинт для обновления профиля
@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """
    Обновление профиля пользователя
    ---
    tags:
      - User Management
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Новый email пользователя
    responses:
      200:
        description: Профиль успешно обновлен
    """
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
    """
    Удаление профиля пользователя
    ---
    tags:
      - User Management
    security:
      - Bearer: []
    responses:
      200:
        description: Профиль успешно удален
    """
    db: Session = SessionLocal()
    db_user = db.query(User).filter_by(username=current_user.username).first()
    db.delete(db_user)
    db.commit()
    db.close()
    return jsonify({'message': 'User deleted successfully'})
