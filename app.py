from flask import Flask
from config import Config
from models import User, Product
from database import Base, engine, SessionLocal
from routes import bp as routes_bp
from products import products_bp

app = Flask(__name__)
app.config.from_object(Config)

# Создание всех таблиц
with app.app_context():
    Base.metadata.create_all(bind=engine)

# Регистрация blueprint
app.register_blueprint(routes_bp)
app.register_blueprint(products_bp)

@app.route('/')
def home():
    return {'message': 'Welcome to the API!'}

if __name__ == '__main__':
    app.run(debug=True)
