from config import Config
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from forms import LoginForm


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Integer, default=1)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User({self.username}, {self.email}, role={self.role})"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    description = db.Column(db.String(200))
    thumbnail = db.Column(db.String(100), default='static/img/default.jpg')
    hide = db.Column(db.Integer, default=0)
    order_number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime)


""" Because Flask-Login knows nothing about databases, it needs the application's help in loading a user.
For that reason, the extension expects that the application will configure a user loader function,
 that can be called to load a user given the ID. """
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    # For GET requests, show the login form.
    # For POST requests, check if user may login.
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            else:
                login_user(user)
                flash('Login successfull.')
                return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html")


@app.route("/dashboard/projects")
def dashboard_projects():
    return render_template("dashboard/projects.html")


@app.route("/dashboard/subscriptions")
def dashboard_subscriptions():
    return render_template("dashboard/subscriptions.html")


@app.route("/dashboard/notify")
def dashboard_notify():
    return render_template("dashboard/notify.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# hasing pw -> pip install flask-bcrypt
# import flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# hashed_pw = bcrypt.generate_password_hash(pw).decode('utf-8')
# bcrypt.check_password_hash(hashed_pw, user_input_pw) // returns boolean
