from flask import Flask,render_template, request, redirect, url_for, jsonify, flash, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField 
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json



app = Flask(__name__)
app.config['SECRET_KEY'] = "mojSECRETkluc"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/users.sqlite3'
app.config['SQLALCHEMY_BINDS'] = {'two' : 'sqlite:///database/mapcontent.sqlite3'}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))

class Map(db.Model):
	__bind_key__ = 'two'
	id = db.Column(db.Integer, primary_key=True)
	#markers = db.Column(db.String(100))
	latitude = db.Column(db.Float, nullable=False)
	longitude = db.Column(db.Float, nullable=False)
	# content = db.Column(db.String(10000))
	# address = db.dbColumn(db.String(1000))

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))



class LoginForm(FlaskForm):
	username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField("password", validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField("password", validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/', methods=["GET", "POST"])
def map():
	if request.method == "POST":
		req = request.get_json()
		lat = req['latitude']
		lng = req['longitude']
		new_coor = Map(latitude=lat, longitude=lng)
		db.session.add(new_coor)
		db.session.commit()
		res = make_response(jsonify({"message" : "JSON received"}), 200)
		return res

	else:
		logged_in = current_user.is_authenticated
		return render_template('map.html', llgi=logged_in)

@app.route('/create_marker', methods=["POST", "GET"])
@login_required
def create_marker():
	if request.method == "POST":
		# marker_content = request.form['marker_content']
		# new_marker = Map(content=marker_content)
		# db.session.add(new_marker)
		# db.session.commit()
		return redirect("/")
	else:
		return render_template('create.html')


@app.route("/upload", methods=['POST', 'GET'])
@login_required
def upload():
	if request.method == "POST":
		file = request.files['inputFile']
		return file.filename



@app.route('/login', methods=['GET', 'POST'])
def login():
	if not current_user.is_authenticated:
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(username=form.username.data).first()
			if user:
				if check_password_hash(user.password, form.password.data):
					login_user(user, remember=form.remember.data)
					return redirect("/")
			flash('Invalid username or password!')
		return render_template("login.html", form=form)
	else:
		return redirect("/")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if not current_user.is_authenticated:
		form = RegisterForm()
		if form.validate_on_submit():
			hashed_password = generate_password_hash(form.password.data, method='sha256')
			new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
			db.session.add(new_user)
			db.session.commit()
			return redirect("/login")
	else:
		return redirect("/")

	return render_template("signup.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
	return render_template("dashboard.html", name=current_user.username)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect("/")


@app.route("/m")
def m():
	global data
	val = Map.query.all()
	data = {}
	for item in val:
		lati = {'latitude' + str(item.id) : item.latitude, 'longitude' + str(item.id): item.longitude}
		data.update(lati)
	return redirect("/marker_data")

@app.route("/marker_data")
def marker_data():
	return jsonify(data)








if __name__ == '__main__': 
    app.run(debug = True)
    db.create_all()