# app/classes/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import classes
from forms import CrudForm
from .. import db
from ..models import Class

@classes.route('/')
@login_required
def index():
	classes = Class().query.all()
	return render_template('classes/index.html', classes=classes)

@classes.route('/create', methods=['GET', 'POST'])
@login_required
def create():
	form = CrudForm();
	if form.validate_on_submit():
		classObj = Class(
			name=form.name.data, description=form.description.data)
		# add User to the database
		db.session.add(classObj)
		db.session.commit()
		flash('You have successfully created a new class')

		# redirect to the login page
		return redirect(url_for('classes.index'))
	else:
		return render_template('classes/credit.html', create=True, form = form)

@classes.route('/<int:class_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(class_id):
	classObj = Class().query.get(class_id);
	form = CrudForm()
	if form.validate_on_submit():
		classObj.name = form.name.data
		classObj.description = form.description.data
		db.session.commit()
		return redirect(url_form('class.edit', class_id=class_id))
	else:
		form = CrudForm(obj=classObj)
		return render_template('classes/credit.html', create=False, form=form)

@classes.route('/<int:class_id>/show')
@login_required
def show(class_id):
	classObj = Class().query.get(class_id);
	return render_template('classes/show.html', classObj=classObj)

@classes.route('/<int:class_id>/delete')
@login_required
def delete(class_id):
	return redirect(url_for('classes.index'))


@classes.route('/<int:class_id>/assign_courses')
@login_required
def assign_courses(class_id):
	return redirect(url_for('classes.index'))
