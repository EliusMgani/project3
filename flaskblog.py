from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '2a8c2d0d3aa9f6d270301cfe74981cfd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db=SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    password = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    

    def __repr__(self):
        return "User('{self.username'), '(self.email)', '(self.image_file )')"


class Post(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100), nullable=False)
     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
     content = db.Column(db.Text, nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

     def __repr__(self):
        return "Post('{self.title'), '(self.date_posted)')"


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account is Created for {form.username.data}!', 'Success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
            flash('You Have Been Logged in..!!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please Check your Username and/or Password and Try Again', 'denger')
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)