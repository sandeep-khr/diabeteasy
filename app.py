from flask import Flask, request, jsonify, render_template, flash, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from sqlalchemy import func
from forms import SignUpForm, LoginForm, PredictForm

app = Flask(__name__)

# create the extension
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
app.secret_key = 'the random string'
# app.app_context().push()
# db.create_all()
login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# define the route for the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, age = form.age.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {user.username}! You can now log in')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@login_required
@app.route('/predict')
def predict_tool():
    return render_template('predict_tool.html')



## Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # dp = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    age = db.Column(db.String(140))
    state = db.Column(db.String(120))
    city = db.Column(db.String(120))
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




if __name__ == '__main__':
    app.run(port=5000, debug=True)