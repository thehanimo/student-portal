from flask import Flask, render_template, Response, request, redirect, url_for, jsonify, abort
app = Flask(__name__)

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, UserInfo
from werkzeug.security import generate_password_hash, check_password_hash


engine = create_engine('sqlite:///user-records.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsess = DBSession()

#Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
	return dbsess.query(User).filter_by(id=user_id).one()        
        


@app.route('/')
@app.route('/home')
@login_required
def home():
	username = current_user.username
	myQuery = dbsess.query(User).filter_by(username=username).one()
	infoQuery = dbsess.query(UserInfo).filter_by(user=myQuery).one() 
	return render_template('home.html', myQuery=myQuery, infoQuery=infoQuery)


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		myQuery = dbsess.query(User).filter_by(username=username).first()
		if myQuery:
			if check_password_hash(myQuery.password, password):
				id = myQuery.id
				user = myQuery
				login_user(user)
				password = ""
				return redirect(url_for('home'))
			else:
				return abort(401)
		else:
			return abort(401)
	else:
		return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
	regText = ""
	if request.method == 'POST':
		username = request.form['username']
		password1 = request.form['password1']
		password2 = request.form['password2']
		name = request.form['name']
		dob = request.form['dob']
		dob = dob.split('-')
		dob = dob[2] + '-' + dob[1] + '-' + dob[0]
		batch = request.form['batch']
		course = request.form['course']
		blood_group = request.form['bgp']
		mobile = request.form['mob']
		fathers_name = request.form['fname']
		emergency = request.form['econ']
		if dbsess.query(User).filter_by(username=username).first():
			regText = "User already registered."
			return render_template('register.html', regText=regText)
		elif password1 != password2:
			regText = "Passwords do not match"
			return render_template('register.html', regText=regText)
		elif len(password1) < 6:
			regText = "Password should be at least 6 characters"
			return render_template('register.html', regText=regText)
		elif len(password1) >= 6:
			hashed = generate_password_hash(password1)
			newStudent = User(username=username, password=hashed)
			dbsess.add(newStudent)
			dbsess.commit()
			newStudentInfo = UserInfo(name=name, dob=dob, batch=batch, course=course, blood_group=blood_group, mobile=mobile, fathers_name=fathers_name, emergency_contact=emergency, user= newStudent)
			dbsess.add(newStudentInfo)
			dbsess.commit()
			regText = "Registered Successfully!"
			return render_template('register.html', regText=regText)
		else:
			return abort(401)
	else:
		return render_template('register.html', regText=regText)


@app.route("/edit", methods=["GET", "POST"])
def edit():
	editText = ""
	if request.method == 'POST':
		username = current_user.username
		myQuery = dbsess.query(User).filter_by(username=username).one()
		usernameNew = request.form['usernameNew']
		password1 = request.form['password1']
		password2 = request.form['password2']
		if dbsess.query(User).filter_by(username=usernameNew).first():
			editText = "Username unavailable."
			return render_template('edit.html', editText=editText)
		elif password1 != password2:
			editText = "Passwords do not match"
			return render_template('edit.html', editText=editText)
		elif len(password1) < 6:
			editText = "Password should be at least 6 characters"
			return render_template('edit.html', editText=editText)
		elif len(password1) >= 6:
			myQuery.username = usernameNew
			hashed = generate_password_hash(password1)
			myQuery.password = hashed
			dbsess.add(myQuery)
			dbsess.commit()
			editText = "Edited Successfully!"
			return redirect(url_for('home'))
		else:
			return abort(401)
	else:
		return render_template('edit.html', editText=editText)



# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
          

    

if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'abcd'
	app.run()
