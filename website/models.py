from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
    
class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(155))
    description = db.Column(db.String(500))
    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))
    options = db.relationship('Option', backref='question', lazy=True)

class Option(db.Model):
    option_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    text = db.Column(db.String(100))
    is_correct = db.Column(db.Boolean)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(1500))
    name=db.Column(db.String(150))
    rating=db.Column(db.Float(precision=2),default=0)
    role = db.Column(db.String(20), default='user')

class Result(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer)
    user_id=db.Column(db.Integer)
    mark=db.Column(db.Integer)
    total_mark=db.Column(db.Integer)
    
    