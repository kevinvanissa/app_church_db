from wtforms import TextField, BooleanField, SelectField, TextAreaField, HiddenField, IntegerField, FormField, PasswordField, SelectMultipleField, FileField, DateTimeField, DecimalField, validators,DateField
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

GENDER = [
    ('','--- Enter Gender ---'),
    ('MALE','MALE'),
    ('FEMALE','FEMALE')
]

OPERATOR = [
    ('','-- op --'),
    ('>','>'),
    ('<','<'),
    ('=','='),
    ('!=','!='),
    ('<=','<='),
    ('>=','>=')
]


DECEASED = [
    ('','--- Deceased? ---'),
    ('DECEASED','DECEASED')
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

COUNTRY = [
    ('JM', 'Jamaica'),
    ('AF', 'Afghanistan'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AS', 'American Samoa'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AI', 'Anguilla'),
    ('AQ', 'Antarctica'),
    ('AG', 'Antigua And Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AW', 'Aruba'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia'),
    ('BA', 'Bosnia And Herzegowina'),
    ('BW', 'Botswana'),
    ('BV', 'Bouvet Island'),
    ('BR', 'Brazil'),
    ('BN', 'Brunei Darussalam'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('CV', 'Cape Verde'),
    ('KY', 'Cayman Islands'),
    ('CF', 'Central African Rep'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CX', 'Christmas Island'),
    ('CC', 'Cocos Islands'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CK', 'Cook Islands'),
    ('CR', 'Costa Rica'),
    ('CI', 'Cote D`ivoire'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('TP', 'East Timor'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('ET', 'Ethiopia'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GF', 'French Guiana'),
    ('PF', 'French Polynesia'),
    ('TF', 'French S. Territories'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GI', 'Gibraltar'),
    ('GR', 'Greece'),
    ('GL', 'Greenland'),
    ('GD', 'Grenada'),
    ('GP', 'Guadeloupe'),
    ('GU', 'Guam'),
    ('GT', 'Guatemala'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('HN', 'Honduras'),
    ('HK', 'Hong Kong'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IL', 'Israel'),
    ('IT', 'Italy'),
    ('JP', 'Japan'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KP', 'Korea (North)'),
    ('KR', 'Korea (South)'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', 'Laos'),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MO', 'Macau'),
    ('MK', 'Macedonia'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MQ', 'Martinique'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('YT', 'Mayotte'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia'),
    ('MD', 'Moldova'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('MS', 'Montserrat'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('AN', 'Netherlands Antilles'),
    ('NC', 'New Caledonia'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('NU', 'Niue'),
    ('NF', 'Norfolk Island'),
    ('MP', 'Northern Mariana Islands'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PN', 'Pitcairn'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('PR', 'Puerto Rico'),
    ('QA', 'Qatar'),
    ('RE', 'Reunion'),
    ('RO', 'Romania'),
    ('RU', 'Russian Federation'),
    ('RW', 'Rwanda'),
    ('KN', 'Saint Kitts And Nevis'),
    ('LC', 'Saint Lucia'),
    ('VC', 'St Vincent/Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('ST', 'Sao Tome'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SH', 'St. Helena'),
    ('PM', 'St.Pierre'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SZ', 'Swaziland'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syrian Arab Republic'),
    ('TW', 'Taiwan'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania'),
    ('TH', 'Thailand'),
    ('TG', 'Togo'),
    ('TK', 'Tokelau'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad And Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('UK', 'United Kingdom'),
    ('US', 'United States'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VA', 'Vatican City State'),
    ('VE', 'Venezuela'),
    ('VN', 'Viet Nam'),
    ('VG', 'Virgin Islands (British)'),
    ('VI', 'Virgin Islands (U.S.)'),
    ('EH', 'Western Sahara'),
    ('YE', 'Yemen'),
    ('YU', 'Yugoslavia'),
    ('ZR', 'Zaire'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe')
]
PARISHES = [
    ('', '-- Choose a Parish --'),
    ('Kingston', 'Kingston'),
    ('St. Andrew', 'St. Andrew'),
    ('St. Catherine', 'St. Catherine'),
    ('St. Ann', 'St. Ann'),
    ('St. James', 'St. James'),
    ('Portland', 'Portland'),
    ('Manchester', 'Manchester'),
    ('Clarendon', 'Clarendon'),
    ('St. Thomas', 'St. Thomas'),
    ('St. Mary', 'St. Mary'),
    ('St. Elizabeth', 'St. Elizabeth'),
    ('Trelawny', 'Trelawny'),
    ('Hanover', 'Hanover'),
    ('Westmoreland', 'Westmoreland')
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
    date = DateField('date', validators=[Required()], format='%Y-%m-%d')
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



class AdvancedSearchForm(FlaskForm):
    gender = SelectField('',choices=GENDER)
    deceased = SelectField('',choices=DECEASED)
    area = TextField('')
    age1 = IntegerField('')
    age2 = IntegerField('')
    operator1 = SelectField('',choices=OPERATOR)
    operator2 = SelectField('',choices=OPERATOR)

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
    gender = SelectField('Gender',choices=GENDER,validators=[Required()])
    dob = DateField('Date of Birth',validators=(validators.Optional(),))
    marriage_date = DateField('Date of Marriage',validators=(validators.Optional(),))
    baptism_date = DateField('Date of Baptism', validators=(validators.Optional(),))
    marital_status = SelectField('Marital Status',choices=MARITAL) 
    no_children = IntegerField('No of Children',validators=(validators.Optional(),))
    employment_status = SelectField('Employment Status',choices=EMP)
    deceased = SelectField('Deceased?',choices=DECEASED)
    picture = FileField('Picture')
    occupation = TextField('Occupation')
    place_of_employment = TextField('Place of Employment')
    certification = TextField('Certification')
    street = TextField('Address 1')
    city = TextField('Address 2')
    state = SelectField('If Jamaica Choose Parish:',choices=PARISHES)
    zip = SelectField('Country',choices=COUNTRY)

class AddUserForm(FlaskForm):
    email = TextField('Email')
    firstname = TextField('First Name', [Required()])
    lastname = TextField('Last Name', [Required()])
    middlename = TextField('Middle Name')
    gender = SelectField('Gender',choices=GENDER, validators=[Required()])
    dob = DateField("Date of Birth",validators=(validators.Optional(),))
    marriage_date = DateField('Date of Marriage',validators=(validators.Optional(),))
    baptism_date = DateField('Date of Baptism',validators=(validators.Optional(),))
    marital_status = SelectField('Marital Status',choices=MARITAL) 
    no_children = IntegerField('No of Children',validators=(validators.Optional(),))
    employment_status = SelectField('Employment Status',choices=EMP)
    picture = FileField('Picture')
    occupation = TextField('Occupation')
    place_of_employment = TextField('Place of Employment')
    certification = TextField('Certification')
    street = TextField('Address 1')
    city = TextField('Address 2')
    state = SelectField('If Jamaica Choose Parish:',choices=PARISHES)
    zip = SelectField('Country',choices=COUNTRY)




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
