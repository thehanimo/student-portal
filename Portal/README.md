database_setup.py creates the database required.
create_admin.py creates a user "admin" with password "admin123"
Only the admin can register new users through "/register" webpage.
project.py is the main flask file which hosts the website in your local server when run and debugs in the termminal.
static consists of css file(s) and templates consists of html file(s), which are default folders where flask looks into.
Project is written in python 2.7 [Most statements are framework-based. Only minor commands like print vary from 3.6].
Requires python2.7 or python 3.6 with SQLAlchemy, flask, flask_login.
