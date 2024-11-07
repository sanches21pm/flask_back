from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from config import Config
from database import Base, engine
from products import products_bp
from categories import categories_bp
from routes import bp as routes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Swagger(app)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    app.register_blueprint(products_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(routes_bp)

    @app.route('/')
    def home():
        """Welcome page
        ---
        responses:
          200:
            description: Returns a welcome message
        """
        return {'message': 'Welcome to the API!'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
