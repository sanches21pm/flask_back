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
            db = SessionLocal()
            current_user = db.query(User).filter_by(username=data['sub']).first()
            db.close()
        except Exception:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(current_user, *args, **kwargs):
            if current_user.role not in roles:
                return jsonify({'message': 'Permission denied'}), 403
            return func(current_user, *args, **kwargs)
        return wrapper
    return decorator
