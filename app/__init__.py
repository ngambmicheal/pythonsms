# app/__init__.py

# third-party imports
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

login_manager = LoginManager()

def create_app(config_name):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_object(app_config[config_name])
  app.config.from_pyfile('config.py')
  db.init_app(app)

  login_manager.init_app(app)
  login_manager.login_message = "You must be logged in to access this page."
  login_manager.login_view = "auth.login"
  
  migrate = Migrate(app, db)
  Bootstrap(app)

  from app import models

  @app.route('/')
  def welcome():
    return redirect(url_for('home.homepage'))

  from .classes import classes as classes_blueprint
  app.register_blueprint(classes_blueprint, url_prefix='/classes')
  
  from .courses import courses as courses_blueprint
  app.register_blueprint(courses_blueprint, url_prefix='/courses')

  from .staffs import staffs as staffs_blueprint
  app.register_blueprint(staffs_blueprint, url_prefix='/staffs')

  from .settings import settings as settings_blueprint
  app.register_blueprint(settings_blueprint, url_prefix='/settings')

  from .students import students as students_blueprint
  app.register_blueprint(students_blueprint, url_prefix='/students')

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix='/auth')

  from .home import home as home_blueprint
  app.register_blueprint(home_blueprint, url_prefix='/home')

  return app
