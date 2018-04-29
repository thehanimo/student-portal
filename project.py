from flask import Flask, render_template, Response, request, redirect, url_for, jsonify, abort
app = Flask(__name__)

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, UserInfo, Attendance
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
    attendQuery = dbsess.query(Attendance).all()
    allQuery = dbsess.query(User).all()
    myQuery = dbsess.query(User).filter_by(username=username).one()
    infoQuery = dbsess.query(UserInfo).filter_by(user=myQuery).one() 
    return render_template('home.html', myQuery=myQuery, infoQuery=infoQuery, allQuery=allQuery)


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
@login_required
def register():
	regText = ""
	if request.method == 'POST':
		if current_user.username != 'admin':
			return render_template(url_for('register'))
		username = request.form['username']
		password1 = request.form['password1']
		password2 = request.form['password2']
		usertype = request.form['usertype']
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
			newStudent = User(username=username, password=hashed, usertype=usertype)
			dbsess.add(newStudent)
			dbsess.commit()
			newStudentInfo = UserInfo(name=name, dob=dob, batch=batch, course=course, blood_group=blood_group, mobile=mobile, fathers_name=fathers_name, emergency_contact=emergency, user= newStudent)
			dbsess.add(newStudentInfo)
			dbsess.commit()
			newStudentAttendance = Attendance(Math_p=0, Math_t=0, Science_p=0, Science_t=0, Art_p=0 , Art_t = 0, English_p = 0, English_t = 0, user = newStudent)
			dbsess.add(newStudentAttendance)
			dbsess.commit()
			regText = "Registered Successfully!"
			return render_template('register.html', regText=regText)
		else:
			return abort(401)
	else:
		return render_template('register.html', regText=regText)


@app.route("/edit", methods=["GET", "POST"])
@login_required
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

@app.route("/delete/<name>", methods=["GET", "POST"])
@login_required
def delete(name):
	if request.method == 'POST':
		myQuery = dbsess.query(User).filter_by(username=name).one()
		infoQuery = dbsess.query(UserInfo).filter_by(user=myQuery).one()
		attendQuery = dbsess.query(Attendance).filter_by(user=myQuery).one()
		dbsess.delete(myQuery)
		dbsess.delete(infoQuery)
		dbsess.commit()
		return redirect(url_for('home'))
	else:
		usernameQuery = dbsess.query(User).filter_by(username=name).first()
		return render_template('delete.html', username=name, usernameQuery=usernameQuery)


@app.route('/edit2/<name>',methods=["GET","POST"])
@login_required
def edit2(name):
	if request.method == 'POST':
		myQuery = dbsess.query(User).filter_by(username=name).one()
		attendQuery = dbsess.query(Attendance).filter_by(user=myQuery).one()
		mathp = request.form['mathp']
		matht = request.form['matht']
		sciencep = request.form['sciencep']
		sciencet = request.form['sciencet']
		artp = request.form['artp']
		artt = request.form['artt']
		englishp = request.form['englishp']
		englisht = request.form['englisht']
		attendQuery.Math_p = mathp
		attendQuery.Math_t = matht
		attendQuery.Science_p = sciencep
		attendQuery.Science_t = sciencet
		attendQuery.Art_p = artp
		attendQuery.Art_t = artt
		attendQuery.English_p = englishp
		attendQuery.English_t = englisht
		dbsess.add(attendQuery)
		dbsess.commit()
		return redirect(url_for('home'))	
	else:
		usernameQuery = dbsess.query(User).filter_by(username=name).first()
		myQuery = dbsess.query(User).filter_by(username=name).first()
		attendQuery = dbsess.query(Attendance).filter_by(user=myQuery).first()
		return render_template("edit2.html", myQuery = myQuery, attendQuery = attendQuery, username = name, usernameQuery=usernameQuery)



@app.route('/attendance')
@login_required
def attendance():
	username = current_user.username
	allQuery = dbsess.query(User).all()
	myQuery = dbsess.query(User).filter_by(username=username).one()
	infoQuery = dbsess.query(UserInfo).filter_by(user=myQuery).one()
	attendQuery = dbsess.query(Attendance).filter_by(user=myQuery).one() 
	return render_template('attendance.html', myQuery=myQuery, infoQuery=infoQuery, allQuery=allQuery, attendQuery=attendQuery)



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
