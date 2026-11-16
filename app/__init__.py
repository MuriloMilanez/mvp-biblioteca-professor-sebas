from flask import Flask
from .models import db

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'chave-segura-biblioteca-professor-sebas'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
