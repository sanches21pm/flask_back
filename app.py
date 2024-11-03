from flask import Flask
from flasgger import Swagger
from config import Config
from database import Base, engine
from products import products_bp  # Импортируем Blueprint для продуктов
from routes import bp as routes_bp  # Импортируем Blueprint для маршрутов пользователя

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация Swagger
swagger = Swagger(app)

# Создание всех таблиц в базе данных
with app.app_context():
    Base.metadata.create_all(bind=engine)

# Регистрация Blueprints
app.register_blueprint(products_bp)
app.register_blueprint(routes_bp)  # Регистрация маршрутов пользователя

@app.route('/')
def home():
    """Приветственная страница
    ---
    responses:
      200:
        description: Возвращает приветственное сообщение
    """
    return {'message': 'Welcome to the API!'}

if __name__ == '__main__':
    app.run(debug=True)
