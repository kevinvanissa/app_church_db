from app import db
from app import app
# coding: utf-8
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1
ACTIVE_USER = 1
INACTIVE_USER = 0



class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    random = db.Column(db.Integer)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    middlename = db.Column(db.String(120))
    dob = db.Column(db.DateTime)
    marriage_date = db.Column(db.DateTime)
    baptism_date = db.Column(db.DateTime)
    marital_status = db.Column(db.String(120))
    no_children = db.Column(db.Integer)
    employment_status = db.Column(db.String(120))
    password = db.Column(db.String(140))
    status = db.Column(db.SmallInteger, default=INACTIVE_USER)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    picture = db.Column(db.String(100))
    occupation = db.Column(db.String(120))
    place_of_employment = db.Column(db.String(120))
    certification = db.Column(db.String(120))
    street = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zip = db.Column(db.String(120))


    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return True


    def is_active(self):
        return self.status == ACTIVE_USER

    def is_admin(self):
        return self.role == ROLE_ADMIN

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Member %r %r>' % (self.firstname, self.lastname)


class NextKin(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    member = db.Column(db.Integer, db.ForeignKey('user.id'))
    phone =  db.Column(db.String(120))
    address =  db.Column(db.String(250))


class SabbathSchool(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120), nullable=False)


class SabbathSchoolMembers(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    classid = db.Column(db.Integer, db.ForeignKey('sabbath_school.id'))
    member = db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher = db.Column(db.Integer,default=0) 

class SabbathSchoolAttend(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    ss_class = db.Column(db.Integer, db.ForeignKey('sabbath_school.id'))
    attend_date = db.Column(db.DateTime)
    member = db.Column(db.Integer, db.ForeignKey('user.id'))


class Family(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(120),nullable=False)


class Church(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    conference = db.Column(db.String(120), nullable=False)


class MemberChurch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    church_id = db.Column(db.Integer, db.ForeignKey('church.id'))


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    phone = db.Column(db.String(120),nullable=False)
    primary_secondary = db.Column(db.String(120))
    network = db.Column(db.String(120))

class Department(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        dept_name = db.Column(db.String(120))

class MemberDepartment(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

class FamilyRelationship(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        family_member = db.Column(db.Integer, db.ForeignKey('user.id'))
        relationship = db.Column(db.String(120))

