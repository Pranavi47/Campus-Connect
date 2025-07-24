from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '22831A7266'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://campus_connect_user:OoyFmIHJodYr5N08T80GHEbmd3P4yYX7@dpg-con7hvsf7o1s73ff246g-a.singapore-postgres.render.com/campus_connect'
    db.init_app(app)

    
    
    login_manager.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app