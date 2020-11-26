from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from .config import SECRET_KEY

config = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 300
}

db = SQLAlchemy()
cache = Cache(config=config)


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    cache.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'You need to be logged in!'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .cconverter.currencyconverter import currencyconverter\
        as converter_blueprint
    app.register_blueprint(converter_blueprint)

    from .dataaccesslayer.DAL import DAL as DAL_blueprint
    app.register_blueprint(DAL_blueprint)

    return app
