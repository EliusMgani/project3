from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



posts = [
    {
        'title': 'Blog Post 1',
        'author': 'Lee',
        'content': 'This is My First Blog Post, Enjoy...!!',
        'date_posted': 'posted on June, 18 2020'
    },
     {
        'title': 'Blog Post 2',
        'author': 'Lee',
        'content': 'This is My Second Blog Post, Enjoy...!!',
        'date_posted': 'posted on June, 19 2020'
    },
     {
        'title': 'Blog Post 3',
        'author': 'Jar',
        'content': 'This is My Third Blog Post, Enjoy...!!',
        'date_posted': 'posted on June, 20 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts= posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations.. Your Account Has Successfull Been Created.!!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please Check your Username and/or Password and Try Again', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('home')


@app.route('/account')
@login_required
def account():
    return render_template('account.html')
