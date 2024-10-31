from flask import Flask
from config import Config
from models import User
from database import Base, engine
from routes import bp as routes_bp

app = Flask(__name__)
app.config.from_object(Config)

# Создание всех таблиц
with app.app_context():
    Base.metadata.create_all(bind=engine)

app.register_blueprint(routes_bp)

@app.route('/')
def home():
    return {'message': 'Welcome to the API!'}

if __name__ == '__main__':
    app.run(debug=True)
