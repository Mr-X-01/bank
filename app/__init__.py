import os
from flask import Flask
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import sqlite3

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'credit_history.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.root_path, 'static', 'uploads')
    )

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from . import db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import credit
    app.register_blueprint(credit.bp)
    app.add_url_rule('/', endpoint='index')

    return app
