from operator import and_
from flask import Blueprint, flash, jsonify, render_template, request, session
from sqlalchemy.orm import sessionmaker
from flask_login import login_required,current_user
from .models import Quiz,Question,Option,User
from . import db
from .models import Quiz,Question,Option
import random
import string
views=Blueprint('views',__name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    quizzes = getQuiz()
    return render_template('home.html', user=current_user, quizzes=quizzes)

def getQuiz():
    quizzes = Quiz.query.all()
    return quizzes
    
@views.route('/quiz', methods=['GET'])
@login_required
def quiz_page():
    quiz_id=request.args.get('quiz_id')
    quiz=Quiz.query.get(quiz_id)
    return render_template("quiz.html",quiz=quiz)

@views.route('/question',methods=['GET'])
def get_question():
    try:
        quiz_id = request.args.get('quiz_id')
        quiz = Quiz.query.get(quiz_id)
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        
        questions_data = [
            {
                'question_id': question.question_id,
                'question': question.question,
                'options': [option.text for option in question.options],
                'option_ids':[option.option_id for option in question.options]
            }
            for question in questions
        ]
        return jsonify({'questions': questions_data})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500
    
    
@views.route('/options',  methods=['POST'])
def get_options():
    data=request.get_json()
    question_id=data['question_id']
    options = Option.query.filter_by(question_id=question_id).all()
    return jsonify({'options':options})

@views.route('resultpage')
def result_page():
    return render_template('result.html',user=current_user)
    

@views.route('/result', methods=['POST'])
def get_result():
    data = request.get_json()
    print("Received Answers:", data)
    quiz_id = str(data.get('quiz_id'))
    answers=data.get('answers')
    opid=list(data['answers'].values())
    print(opid)
    print(answers)
    options = db.session.query(Option).filter(
        and_(
            Option.option_id.in_(opid),
            Option.is_correct == True  
        )
    ).all()
    question_ids = Question.query.filter_by(quiz_id=quiz_id).with_entities(Question.question_id).all()
    return jsonify({"ans": len(options),"totalquestion":len(question_ids)})
    
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

