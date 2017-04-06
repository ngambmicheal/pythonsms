import os
import config

from flask import render_template

from . import app

hi = os.environ.get("hi", 5000)

@app.route('/')
def hello_world():
    return render_template('index.html', hello=hi)
