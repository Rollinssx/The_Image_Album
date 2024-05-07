from flask import render_template, redirect, request, flash, url_for
from flask_login import login_user, login_required
import bcrypt
import logging
from sqlalchemy.exc import IntegrityError, DataError
from image_app.models import User
from image_app.forms import LoginForm, RegistrationForm
from image_app import app, db

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', title='Home page')


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_page():
    return render_template('upload_page.html', title='Upload Page')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
            login_user(user, remember=form.remember.data)
            return redirect(request.args.get('next') or url_for('home_page'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'error')
    return render_template('login.html', title='Log In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.hashpw(form.password.data.encode(), bcrypt.gensalt())
            user = User(username=form.username.data, email=form.email.data, password=hashed_password.decode())
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('login_page'))
        except IntegrityError:
            flash('Username or email already exists.', 'error')
            db.session.rollback()
        except DataError:
            flash('Invalid data. Please check your input.', 'error')
            db.session.rollback()
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
            logging.error(f"Error creating user: {e}")
            db.session.rollback()
    return render_template('signup.html', title='Register', form=form)
