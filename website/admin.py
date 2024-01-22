
from flask import Blueprint, flash, redirect, render_template, request, url_for,flash
from flask_login import login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User,Quiz,Question,Option
from . import db

admin=Blueprint('admin',__name__)

@admin.route('/dashboard')
@login_required
def admin_dashboard():
    if current_user.role !='admin':
        return redirect(url_for('views.home'))
    
    return render_template('admin/dashboard.html')

@admin.route('/addadmin')
def add_admin():
    new_admin_user = User(email='admin1@gmail.com', password=generate_password_hash("manasbariha", method='pbkdf2:sha256',), name='Admin', role='admin')
    db.session.add(new_admin_user)
    db.session.commit()
    print(new_admin_user)

    return "Admin added successfully"

@admin.route('/addquiz',methods=['GET','POST'])
@login_required
def add_question():
    if current_user.role !='admin':
        return redirect(url_for('views.home'))
    if request.method=='POST':
        title=request.form.get('title')
        description=request.form.get('description')
        quiz=Quiz(title=title,description=description)
        db.session.add(quiz)
        db.session.commit()
        flash('one quiz added',category='success')
        
    return render_template('admin/addquiz.html')

@admin.route('/user',methods=['GET'])
@login_required
def user_table():
    if current_user.role !='admin':
        return redirect(url_for('views.home'))
    
    users=getUsers()
    return render_template('admin/user-table.html',users=users)

@admin.route('/quiz')
@login_required
def quiz_table():
    if current_user.role !='admin':
        return redirect(url_for('views.home'))    
    quizzes=getQuiz()
    return render_template('admin/quiz-table.html',quizzes=quizzes)
    
@admin.route('/question')
@login_required
def question_table():
    if current_user.role !='admin':
        return redirect(url_for('views.home'))

    questions=getQuestion()
    return render_template('admin/question-table.html',questions=questions)
    
@admin.route('/addque',methods=['GET','POST'])
@login_required
def add_question_page():
    if current_user.role != 'admin':
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        # Get data from the form
        question_text = request.form.get('question')
        quiz_title = request.form.get('quiz_title')
        option1_text = request.form.get('option1')
        option2_text = request.form.get('option2')
        option3_text = request.form.get('option3')
        option4_text = request.form.get('option4')
        correct_option = request.form.get('correct_option')

        # Find the quiz by title
        quiz = Quiz.query.filter_by(title=quiz_title).first()

        if quiz:
            new_question = Question(question=question_text, quiz_id=quiz.quiz_id)
            db.session.add(new_question)
            db.session.commit()

            option1 = Option(text=option1_text, is_correct=(correct_option == 'option1'), question=new_question)
            option2 = Option(text=option2_text, is_correct=(correct_option == 'option2'), question=new_question)
            option3 = Option(text=option3_text, is_correct=(correct_option == 'option3'), question=new_question)
            option4 = Option(text=option4_text, is_correct=(correct_option == 'option4'), question=new_question)

            db.session.add_all([option1, option2, option3, option4])
            db.session.commit()

            flash('Question added successfully!', category='success')
            return redirect(url_for('admin.add_question_page'))

        else:
            flash('Quiz not found!', category='error')

    quizzes = Quiz.query.all()
    return render_template('admin/add_que.html', quizzes=quizzes)

 
def getUsers():
    users = User.query.filter_by(role='user').all()
    return users

def getQuestion():
    que=Question.query.all()
    return que

def getQuiz():
    quiz=Quiz.query.all()
    return quiz

