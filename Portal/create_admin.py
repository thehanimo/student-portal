from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, UserInfo, Attendance

from werkzeug.security import generate_password_hash

engine = create_engine('sqlite:///user-records.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

password = "admin123"
hashed = generate_password_hash(password)
admin = User(username="admin", password=hashed, usertype="A")

session.add(admin)
session.commit()

adminInfo = UserInfo(name="Administrator", dob="", batch="", course="", blood_group="", mobile="", fathers_name="", emergency_contact="", user=admin)

session.add(adminInfo)
session.commit()

adminAttendance = Attendance(Math_p=0, Math_t=0, Science_p=0, Science_t=0, Art_p=0 , Art_t = 0, English_p = 0, English_t = 0, user = admin)

session.add(adminAttendance)
session.commit()

print "added admin!"