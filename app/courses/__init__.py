# app/admin/__init__.py

from flask import Blueprint

courses = Blueprint('courses', __name__)

from . import views
