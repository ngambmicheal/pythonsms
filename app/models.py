# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


############################ The Users model #####################################
class User(UserMixin, db.Model):
    """
    Create a Users table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    phone = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    student = db.relationship('Student', backref='User',
                            lazy='select', uselist=False)
    staff = db.relationship('Staff', backref='User',
                            lazy='select', uselist=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

############################ The Classes model #####################################

classes_courses = db.Table('classes_courses',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'))
)

class Class(db.Model):
    """
    Create a Classes table
    """

    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    students = db.relationship('Student', backref='class',
                                lazy='dynamic')
    courses = db.relationship('Course', secondary=classes_courses,
        backref=db.backref('classes', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Class: {}>'.format(self.name)

############################ The Students model #####################################

courses_students = db.Table('courses_students',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'))
)

class Student(db.Model):
    """
    Create a Students table
    """

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    courses = db.relationship('Course', secondary=courses_students,
        backref=db.backref('students', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Class: {}>'.format(self.name)

############################ The Courses model #####################################

courses_staffs = db.Table('courses_staffs',
    db.Column('staff_id', db.Integer, db.ForeignKey('staffs.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)

class Course(db.Model):
    """
    Create a Courses table
    """

    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    staffs = db.relationship('Staff', secondary=courses_staffs,
        backref=db.backref('courses', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Course: {}>'.format(self.name)

############################ The Staffs model #####################################

class Staff(db.Model):
    """
    Create a staffs table
    """

    __tablename__ = 'staffs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Staff: {}>'.format(self.name)
