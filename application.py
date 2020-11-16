from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_wtform import *
from models import *
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from time import localtime, strftime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')

#Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

socketio = SocketIO(app)
ROOMS = ["room"]

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/registration", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        hashed_password = pbkdf2_sha512.hash(password)

        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("index.html", form = reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Please login.', 'danger')
        return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully.', 'success')
    return redirect(url_for('login'))

@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + "chat."}, room=data['room'])

@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + "chat."}, room=data['room'])

@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send({'msg' : data['msg'], 'username': data['username'], 'time_stamp': strftime('%d-%b %I:%M %p', localtime())}, room = data['room'])

if __name__ == '__main__':
    app.run()

