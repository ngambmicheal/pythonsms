# app/admin/__init__.py

from flask import Blueprint

staffs = Blueprint('staffs', __name__)

from . import views
