from flask import Flask
from flasgger import Swagger
from app.database import db
from app.routes import atividades_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atividades.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    Swagger(app)
    app.register_blueprint(atividades_bp)

    with app.app_context():
        db.create_all()
    return app
