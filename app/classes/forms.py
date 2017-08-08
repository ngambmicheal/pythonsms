# app/classes/forms.py

from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

class CrudForm(FlaskForm):
    """
    Form for users to create new account
    """
    name = StringField('Class Name', validators=[DataRequired()])
    description = TextAreaField('Class Description', validators=[DataRequired()])
    submit = SubmitField('Save Class')
