import jwt
import datetime
from flask import request, jsonify
from functools import wraps
from models import User
from database import SessionLocal


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, 'your_secret_key', algorithms=["HS256"])
            db = SessionLocal()  # создаем сессию для взаимодействия с базой данных
            current_user = db.query(User).filter_by(username=data['sub']).first()
            db.close()
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user.role != required_role:
                return jsonify({'message': 'Access denied. You do not have permission to perform this action.'}), 403
            return f(current_user, *args, **kwargs)

        return decorated

    return decorator
