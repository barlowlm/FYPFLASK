import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_dropzone import Dropzone
from flaskd3.config import Config


db = SQLAlchemy()
brcypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
dropzone = Dropzone()

## need to edit this configuration

mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    brcypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    dropzone.init_app(app)

    from flaskd3.users.routes import users
    from flaskd3.posts.routes import posts
    from flaskd3.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app

