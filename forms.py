from wtforms import TextField, BooleanField, SelectField, TextAreaField, HiddenField, IntegerField, FormField, PasswordField, SelectMultipleField, FileField, DateTimeField, DecimalField, validators
from wtforms.validators import Required, Length, Email, EqualTo, ValidationError
from app import db

from .models import User, ROLE_ADMIN, INACTIVE_USER, Phone, Department, MemberDepartment, FamilyRelationship,Family,SabbathSchool


from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField


STATUS = [
    ('0', '0'),
    ('1', '1')
]

ANSWER = [
    ('YES', 'YES'),
    ('NO', 'NO')
]

TEACHER =[
        ('','--- Teacher? ---'),
        ('1','Leader'),
        ('2','Assistant')
]



MARITAL = [
      ('','--- Choose Marital Status ---'),
      ('MARRIED','MARRIED'),
      ('SINGLE','SINGLE'),
      ('DIVORCED','DIVORCED'),
      ('WIDOWED','WIDOWED')
]



EMP = [ 
      ('','--- Choose Employment Status ---'),
      ('EMPLOYED','EMPLOYED'),
      ('UNEMPLOYED','UNEMPLOYED')  
]




SALUTATION = [
    ('DR', 'DR'),
    ('MS', 'MS'),
    ('MR', 'MR'),
    ('MRS', 'MRS'),
    ('NA', 'NA'),
    ('TBA1', 'TBA1'),
    ('TBA2', 'TBA2')
]


PRIMARY_SECONDARY=[
    ('', '-- Choose Primary or Secondary --'),
    ('PRIMARY', 'PRIMARY'),
    ('SECONDARY', 'SECONDARY')
]

NETWORK=[
    ('', '-- Choose Digicel or Lime --'),
    ('DIGICEL','DIGICEL'),
    ('LIME','LIME')
]



# def getDepartments():
    # result = []
    # result = [("", "-- Choose a Department --")]
    # departments = Department.query.order_by(Department.dept_name).all()
    # for department in departments:
        # result.append((str(department.id), department.dept_name))
    # return result

# def getUsers():
    # result = []
    # result = [("", "-- Choose a Member --")]
    # users = User.query.order_by(User.lastname).all()
    # print("Testing Here")
    # for user in users:
        # result.append((str(user.id), user.firstname + ' ' + user.lastname))
    # return result

# def getFamilyTypes():
    # result = []
    # result = [("", "-- Choose a Relationship --")]
    # relationships = Family.query.order_by(Family.type).all()
    # for relationship in relationships:
        # result.append((str(relationship.id), relationship.type))
    # return result


# DEPT=getDepartments()
# USERS=getUsers()
# TYPES=getFamilyTypes()


class AddDepartmentForm(FlaskForm):
    dept_name = TextField('Department Name',[Required()])



class DepartmentForm(FlaskForm):
    dept_name = SelectField('Department Name',validators=[Required()])

    def __init__(self):
        super(DepartmentForm,self).__init__()
        self.dept_name.choices =   [("", "-- Choose a Department --")]+[(str(d.id), d.dept_name) for d in Department.query.order_by(Department.dept_name).all()]


class FamilyForm(FlaskForm):
    user = SelectField('Member Name',validators=[Required()])
    type = SelectField('Relationship',validators=[Required()])

    def __init__(self):
        super(FamilyForm,self).__init__()
        self.user.choices =   [("", "-- Choose a Member --")]+[(str(c.id), c.firstname+' '+c.lastname) for c in User.query.order_by(User.lastname).all()]
        self.type.choices =   [("", "-- Choose a Relationship --")]+[(str(f.id), f.type) for f in Family.query.order_by(Family.type).all()]



class AttendanceForm(FlaskForm):
    date = DateTimeField('date', validators=[Required()], format='%Y-%m-%d')
    member = HiddenField('member')
    ss_class = HiddenField('ss_class')


class SearchForm(FlaskForm):
    term = TextField('',[Required()])


class SabbathSchoolForm(FlaskForm):
    name = TextField("Class Name", [Required()])

class SabbathSchoolMemberForm(FlaskForm):
    member = SelectField('Member',validators=[Required()])
    teacher = SelectField('Teacher',choices=TEACHER)
    def __init__(self):
        super(SabbathSchoolMemberForm,self).__init__()
        self.member.choices =   [("", "-- Choose a Member --")]+[(str(c.id), c.firstname+' '+c.lastname) for c in User.query.order_by(User.lastname).all()]

class OtherSabbathSchoolMemberForm(FlaskForm):
    classes = SelectField('Class Name',validators=[Required()])
    member = SelectField('Member',validators=[Required()])
    def __init__(self):
        super(OtherSabbathSchoolMemberForm,self).__init__()
        self.member.choices =   [("", "-- Choose a Member --")]+[(str(c.id), c.firstname+' '+c.lastname) for c in User.query.order_by(User.lastname).all()]
        self.classes.choices =   [("", "-- Choose a Class --")]+[(str(s.id), s.name) for s in SabbathSchool.query.order_by(SabbathSchool.name).all()]



class DepartmentMemberForm(FlaskForm):
    member = SelectField('Member',validators=[Required()])
    def __init__(self):
        super(DepartmentMemberForm,self).__init__()
        self.member.choices =   [("", "-- Choose a Member --")]+[(str(c.id), c.firstname+' '+c.lastname) for c in User.query.order_by(User.lastname).all()]



class LoginForm(FlaskForm):
    email = TextField('email', [Required(), Email()])
    password = PasswordField('password', [Required()])

    remember_me = BooleanField('remember_me', default=False)



class ResetPasswordForm(FlaskForm):
    email = TextField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Confirm', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])




class UploadForm(FlaskForm):
    filexl = FileField(validators=[Required()])


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('oldpassword', [Required()])
    password = PasswordField('password', [Required()])
    confirm = PasswordField('confirm', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])


class ManageUserForm(FlaskForm):
    password = PasswordField('password')
    confirm = PasswordField(
        'confirm', [
            EqualTo(
                'password', message='Passwords must match')])
    status = SelectField('status', choices=STATUS, validators=[Required()])
    uwiId = TextField('uwiId', validators=[Required()])
    userInitial = TextField('userInitial', validators=[Required()])
    salutation = SelectField(
        'salutation',
        choices=SALUTATION,
        validators=[
            Required()])
    marker = SelectField('marker', choices=ANSWER, validators=[Required()])
    tutor = SelectField('tutor', choices=ANSWER, validators=[Required()])
    lecturer = SelectField('lecturer', choices=ANSWER, validators=[Required()])


class EditUserForm(FlaskForm):
    email = TextField('Email')
    firstname = TextField('First Name', [Required()])
    lastname = TextField('Last Name', [Required()])
    middlename = TextField('Middle Name')
    dob = DateTimeField('Date of Birth',validators=(validators.Optional(),))
    marriage_date = DateTimeField('Date of Marriage',validators=(validators.Optional(),))
    baptism_date = DateTimeField('Date of Baptism', validators=(validators.Optional(),))
    marital_status = SelectField('Marital Status',choices=MARITAL) 
    no_children = IntegerField('No of Children',validators=(validators.Optional(),))
    employment_status = SelectField('Employment Status',choices=EMP)
    picture = FileField('Picture')
    occupation = TextField('Occupation')
    place_of_employment = TextField('Place of Employment')
    certification = TextField('Certification')
    street = TextField('Address 1')
    city = TextField('Address 2')
    state = TextField('Address 3')
    zip = TextField('Country')


class AddUserForm(FlaskForm):
    email = TextField('Email')
    firstname = TextField('First Name', [Required()])
    lastname = TextField('Last Name', [Required()])
    middlename = TextField('Middle Name')
    dob = DateTimeField("Date of Birth",validators=(validators.Optional(),))
    marriage_date = DateTimeField('Date of Marriage',validators=(validators.Optional(),))
    baptism_date = DateTimeField('Date of Baptism',validators=(validators.Optional(),))
    marital_status = SelectField('Marital Status',choices=MARITAL) 
    no_children = IntegerField('No of Children',validators=(validators.Optional(),))
    employment_status = SelectField('Employment Status',choices=EMP)
    picture = FileField('Picture')
    occupation = TextField('Occupation')
    place_of_employment = TextField('Place of Employment')
    certification = TextField('Certification')
    street = TextField('Address 1')
    city = TextField('Address 2')
    state = TextField('Address 3')
    zip = TextField('Country')




class EditPhoneForm(FlaskForm):
    phone = TextField('Phone',validators=[Required()])
    #primary_secondary = TextField('Primary or Secondary')
    primary_secondary = SelectField('Primary or Secondary',choices=PRIMARY_SECONDARY,validators=[Required()])
    network = SelectField('Network',choices=NETWORK)

#class EditDepartmentForm(Form):


class RegistrationForm(FlaskForm):
    firstname = TextField('firstname', [Required()])
    lastname = TextField('lastname', [Required()])
    email = TextField('email', [Required(), Email()])
    password = PasswordField('password', [Required()])
    confirm = PasswordField('confirmpassword', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])


# class LoginForm(FlaskForm):
    # username = TextField('username')
    # password = PasswordField('password')
