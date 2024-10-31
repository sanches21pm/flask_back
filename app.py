from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


# Создание базы данных
with app.app_context():
    db.create_all()


# Функция декоратора для проверки токена
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            token = token.split(" ")[1]  # Получаем токен из строки 'Bearer <token>'
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['sub']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# Эндпоинт для регистрации
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


# Эндпоинт для получения токена
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 400

    token = jwt.encode({'sub': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'access_token': token, 'token_type': 'bearer'})


# Защищенный эндпоинт для получения профиля
@app.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({'username': current_user.username, 'email': current_user.email})


# Защищенный эндпоинт для обновления профиля
@app.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.get_json()
    current_user.email = data.get('email', current_user.email)
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'})


# Защищенный эндпоинт для удаления профиля
@app.route('/profile', methods=['DELETE'])
@token_required
def delete_profile(current_user):
    db.session.delete(current_user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})


# Эндпоинт для тестирования
@app.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'Test successful'})


if __name__ == '__main__':
    app.run(debug=True)
