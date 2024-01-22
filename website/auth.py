from flask import Blueprint,render_template, request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Login successfully!',category='success')
                login_user(user, remember=True)
                if user.role=='admin':
                    return redirect(url_for('admin.admin_dashboard'))
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password,try again.",category="error")
        else:
            flash('Email does not exist',category='error')
    data=request.form
    print(data)
    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        password=request.form.get('password')
        cpassword=request.form.get('confirm-password')
        
        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        if len(email) < 4 :
            flash('Email must be greater than 4 charecter',category='error')
            pass
        elif len(name) < 2:
            flash('nmae must be greater than 2 charecter',category='error')
            pass
        elif password !=cpassword:
            flash('Password do not  match',category='error')
            pass
        elif len(password) < 7:
            flash('password must be greater than 7 charecter',category='error')
            pass
        else:
            
            new_user = User(email=email, name=name,password=generate_password_hash(password, method='pbkdf2:sha256',))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created',category='success')
            return redirect(url_for('views.home'))
            
            
    return render_template('signup.html',user=current_user)