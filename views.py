# from myapp import app
# from models import Member
# from forms import LoginForm
# from flask import render_template

# @app.route('/')
# def index():
    # # firstmember = Member.query.first()
    
    # return '<h1>The first member is: '+ 'kevin' +'</h1>'

# @app.route('/login')
# def login():
    # form = LoginForm()
    # return render_template('index.html', form=form)


from flask import render_template, jsonify
from app import app, db, lm
from .models import User, ROLE_ADMIN, INACTIVE_USER, Phone, Department, MemberDepartment, FamilyRelationship, Church, MemberChurch,Family,SabbathSchool,SabbathSchoolAttend,SabbathSchoolMembers
from .forms import LoginForm, UploadForm, ChangePasswordForm, RegistrationForm,EditUserForm,EditPhoneForm,DepartmentForm,FamilyForm,AddUserForm,AttendanceForm, SabbathSchoolForm,SabbathSchoolMemberForm,SearchForm, ResetPasswordForm,AddDepartmentForm,DepartmentMemberForm,OtherSabbathSchoolMemberForm, AdvancedSearchForm
from werkzeug import check_password_hash, generate_password_hash, secure_filename
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, send_from_directory, abort
import uuid
from flask_login import login_user, logout_user, current_user, login_required
from config import ALLOWED_EXTENSIONS
from functools import wraps, reduce
import os
import csv
import time as pytime
import datetime,time, calendar
from sqlalchemy import text, func

def debug(aVariable):
    print("*****************>>> Printing Variable: ",aVariable)


def active_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.status == INACTIVE_USER:
            flash("Please wait for activation", category='danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(413)
def internal_error(error):
    db.session.rollback()
    return render_template('413.html'), 413


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def login():
    # if g.user is not None:
    # if g.user is not None and g.user.is_authenticated():
        # return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(
                'The username or password you entered is incorrect!',
                category='danger')
            return redirect(url_for('login'))
        if user.password is None or user.password == "":
            flash(
                'The username or password you entered is incorrect!',
                category='danger')
            return redirect(url_for('login'))
        if user and check_password_hash(
                user.password,
                form.password.data) and user.is_active():
            session['remember_me'] = form.remember_me.data
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
            flash('You have successfully logged in', category='success')
            return redirect(request.args.get('next') or url_for('main'))

        if user and not check_password_hash(
                user.password, form.password.data) and user.is_active():
            flash('Please check your username and password!', category='danger')
            return redirect(url_for('login'))

        if user and check_password_hash(
                user.password,
                form.password.data) and not user.is_active():
            flash("Your account needs activation!", category='warning')
            return redirect(url_for('login'))

        if user and not check_password_hash(
                user.password,
                form.password.data) and not user.is_active():
            flash("Your account needs activation!", category='warning')
            return redirect(url_for('login'))

    return render_template('login.html',
                           title='Sign In',
                           form=form)



@app.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    form = ResetPasswordForm()
    user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your password was successfully reset!', category='success')
        return redirect(url_for('main'))
    return render_template('reset.html', form=form)





@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('There is already a user with this email!', category='danger')
            return redirect(url_for('register'))
        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            password=generate_password_hash(
                form.password.data))
        db.session.add(user)
        db.session.commit()
        flash(
            'Thanks for registering. Your account will need activation.',
            category='info')
        return redirect(url_for('login'))
    return render_template(
        'register.html',
        title='Register',
        form=form,
        )



@app.route('/reports',methods=['GET','POST'])
@login_required
def reports():
    import operator 

    op = {
            '>':operator.gt,
            '<':operator.lt,
            '=':operator.eq,
            '!=':operator.ne,
            '<=':operator.le,
            '>=':operator.ge
        }
    form = AdvancedSearchForm()
    gender = request.args.get("gender")
    deceased = request.args.get("deceased")
    area = request.args.get("area")
    age1 = request.args.get("age1")
    age2 = request.args.get("age2")
    operator1 = request.args.get("operator1")
    operator2 = request.args.get("operator2")

    query_dict = dict() 
    if gender:
        query_dict['gender'] = gender 

    if deceased:
        query_dict['deceased'] = deceased



    users = User.query.filter_by(**query_dict)

    query_list = []
    if area:
        query_list.append(User.street.ilike("%"+area+"%"))
        query_list.append(User.city.ilike("%"+area+"%"))
        users = users.filter(
                reduce(
                    lambda a, b:(
                        a | b),query_list))



    userages = users.order_by(User.lastname).all()
    if age1 and age2 and operator1 and operator2:
        # users = [u for u in userages if u.get_age() > 30 and u.get_age() < 50 ]
        users = [u for u in userages if op[operator1](u.get_age(),int(age1)) and  op[operator2](u.get_age(),int(age2))]
    
    if age1 and operator1:
        users = [u for u in userages if op[operator1](u.get_age(),int(age1))]


    if age2 and operator2:
        # debug(age2)
        # debug(operator2)
        users = [u for u in userages if op[operator2](u.get_age(),int(age2))]


    return render_template('reports.html',form=form,users=users)


@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    form = AddUserForm()
    form2 = SearchForm()
    users = []
    term = request.args.get('term')

    #===========================================================
    import operator 

    op = {
            '>':operator.gt,
            '<':operator.lt,
            '=':operator.eq,
            '!=':operator.ne,
            '<=':operator.le,
            '>=':operator.ge
        }
    form3 = AdvancedSearchForm()
    gender = request.args.get("gender")
    deceased = request.args.get("deceased")
    area = request.args.get("area")
    age1 = request.args.get("age1")
    age2 = request.args.get("age2")
    operator1 = request.args.get("operator1")
    operator2 = request.args.get("operator2")

    query_dict = dict() 
    if gender:
        query_dict['gender'] = gender 

    if deceased:
        query_dict['deceased'] = deceased



    users = User.query.filter_by(**query_dict)

    query_list = []
    if area:
        query_list.append(User.street.ilike("%"+area+"%"))
        query_list.append(User.city.ilike("%"+area+"%"))
        users = users.filter(
                reduce(
                    lambda a, b:(
                        a | b),query_list))


        #===========================================================

    #FIXME: These need to fix like the above
    query_list2 = []
    if term:
        mterm = term.split(" ")
        if len(mterm) == 2:
            query_list2.append(User.firstname.ilike("%"+mterm[0]+"%"))
            query_list2.append(User.lastname.ilike("%"+mterm[1]+"%"))
            users = users.filter(
                    reduce(
                        lambda a, b:(
                            a & b), query_list2))

            # users = User.query.order_by(User.lastname).filter((User.firstname.like('%'+mterm[0]+'%')),(User.lastname.like('%'+mterm[1]+'%')) ).all()
        else:
            query_list2.append(User.firstname.ilike("%"+term+"%"))
            query_list2.append(User.lastname.ilike("%"+term+"%"))
            users = users.filter(
                    reduce(
                        lambda a, b: (
                            a | b),query_list2))

            # users = User.query.order_by(User.lastname).filter((User.firstname.like('%'+term+'%')) | (User.lastname.like('%'+term+'%')) ).all()
    # else:
        # users = User.query.order_by(User.lastname).all()

    users = users.order_by(User.lastname).all()


    if age1 and age2 and operator1 and operator2:
        # users = [u for u in userages if u.get_age() > 30 and u.get_age() < 50 ]
        users = [u for u in users if op[operator1](u.get_age(),int(age1)) and  op[operator2](u.get_age(),int(age2))]
    
    if age1 and operator1:
        users = [u for u in users if op[operator1](u.get_age(),int(age1))]


    if age2 and operator2:
        debug(age2)
        debug(operator2)
        users = [u for u in users if op[operator2](u.get_age(),int(age2))]



    if form.validate_on_submit():

            filename = ""
            file = request.files['picture']
            if file:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename=str(uuid.uuid4())+filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                else:
                    flash('Only jpeg, jpg or png files are accepted',category='danger')
                    return redirect(url_for('main'))
            user = User(
                email = form.email.data,
                firstname = form.firstname.data,
                lastname = form.lastname.data,
                middlename = form.middlename.data,
                dob = form.dob.data,
                marriage_date = form.marriage_date.data,
                baptism_date = form.baptism_date.data,
                marital_status = form.marital_status.data,
                no_children = form.no_children.data,
                employment_status = form.employment_status.data,
                picture = filename,
                occupation = form.occupation.data,
                place_of_employment = form.place_of_employment.data,
                certification = form.certification.data,
                street = form.street.data,
                city  = form.city.data,
                state = form.state.data,
                zip  = form.zip.data)
            db.session.add(user)
            db.session.commit()
            flash('User has been Added',category='success')
            return redirect(url_for('main'))
    return render_template(
            'main.html',
            title='Members',
            users=users,
            form=form,
            form2=form2,
            form3=form3
            )



@app.route('/dept_members/<int:id>', methods=['GET', 'POST'])
@login_required
def dept_members(id):
    department = Department.query.get_or_404(id)
    form = DepartmentMemberForm()
    dmembers = db.session.query(User,MemberDepartment).filter(User.id==MemberDepartment.user_id,MemberDepartment.department_id==department.id).all()
    if form.validate_on_submit():
        user = MemberDepartment(
            department_id = department.id,
            user_id = form.member.data)
        db.session.add(user)
        db.session.commit()
        flash('User has been Added to the Department',category='success')
        return redirect(url_for('dept_members',id=id))

    return render_template(
            'dept_members.html',
            title='Department Members',
            dmembers=dmembers,
            department=department,
            form=form,
            )




@app.route('/ss_members/<int:id>', methods=['GET', 'POST'])
@login_required
def ss_members(id):
    # users = User.query.all()
    sschool = SabbathSchool.query.get_or_404(id)
    ssteachers = db.session.query(User,SabbathSchoolMembers).filter(User.id==SabbathSchoolMembers.member,SabbathSchoolMembers.classid==sschool.id).filter((SabbathSchoolMembers.teacher==1) | (SabbathSchoolMembers.teacher==2)).all()
    # print(ssteachers)
    # schoolname = sschool.name
    # print(schoolname)
    form = SabbathSchoolMemberForm()
    ssmembers = db.session.query(User,SabbathSchoolMembers).filter(User.id==SabbathSchoolMembers.member,SabbathSchoolMembers.classid==sschool.id).all()
    ssmembers2 = db.session.query(User,SabbathSchoolMembers).filter(User.id==SabbathSchoolMembers.member).all()
    # print(ssmembers2)
    if form.validate_on_submit():
        for m in ssmembers2:
            if m.SabbathSchoolMembers.member == int(form.member.data):
                flash('This memeber is already in another class',category='danger')
                return redirect(url_for('ss_members',id=id))
        #TODO: Check if member is already in a sabbath school or is already a member in this classid
        teacher = 0
        if form.teacher.data:
            teacher = int(form.teacher.data)
        user = SabbathSchoolMembers(
            classid = sschool.id,
            member = form.member.data,
            teacher = teacher)
        db.session.add(user)
        db.session.commit()
        flash('User has been Added class',category='success')
        return redirect(url_for('ss_members',id=id))


    mnames = "January February March April May June July August September October November December"
    mnames = mnames.split()
 
    #Creating data for the graph
    today = datetime.datetime.now()
    year = today.year
    total_visits = 0
    mycal = dict() 
    for i in range(12):
        cal = calendar.Calendar(6)
        month_days = cal.itermonthdays(year, (i+1))
        month = []
        count = 1

        for day in month_days:
            if (count % 7 == 0) and (day != 0) :
                attend = SabbathSchoolAttend.query.filter_by(attend_date=datetime.datetime(year,i+1,day),ss_class=id).all()           
                if attend:
                    total_visits = total_visits + 1
                else:
                    pass
            count = count + 1
        
        month.append(total_visits)
        mycal[mnames[i]] = month
        total_visits = 0

    return render_template(
            'ss_members.html',
            title='Members',
            ssmembers=ssmembers,
            sschool=sschool,
            form=form,
            mycal=mycal,
            mnames=mnames,
            ssteachers=ssteachers
            )





@app.route('/sschools', methods=['GET', 'POST'])
@login_required
def sschools():
    form = SabbathSchoolForm()
    # sclasses =  SabbathSchool.query.all()

    sclasses = db.session.query(SabbathSchool).order_by(SabbathSchool.name).all()
    # print(sclasses)

    if form.validate_on_submit():
        school = SabbathSchool(name=form.name.data)
        db.session.add(school)
        db.session.commit()
        flash('The class was successfully created',category='success')
        return redirect(url_for('sschools'))

#    if form2.validate_on_submit():


    return render_template(
            'sabbathschools.html',
            title='Sabbath Schools',
            form=form,
            sclasses=sclasses
            )




@app.route('/deregister/<int:id>/<int:sid>', methods=['GET', 'POST'])
@login_required
def deregister(id,sid):
    # user = User.query.get_or_404(id)
    # sschool = SabbathSchool.query.get_or_404(sid)
    user = SabbathSchoolMembers.query.filter_by(member=id,classid=sid).first()
    print(user)
    db.session.delete(user)
    db.session.commit()
    flash('The user was deregistered',category='success')
    return redirect(url_for('ss_members',id=sid))

@app.route('/deregisterdept/<int:id>/<int:did>', methods=['GET', 'POST'])
@login_required
def deregisterdept(id,did):
    user = MemberDepartment.query.filter_by(user_id=id,department_id=did).first()
    print(user)
    db.session.delete(user)
    db.session.commit()
    flash('The user was deregistered from the department',category='success')
    return redirect(url_for('dept_members',id=did))





@app.route('/delete_attend/<int:year>/<int:month>/<int:day>/<int:id>/<int:sid>',methods=['GET','POST'])
@login_required
def delete_attend(year,month,day,id,sid):
    # result_sql = text("SELECT id from sabbath_school_attend  sa WHERE YEAR(sa.attend_date)=:y AND  MONTH(sa.attend_date)=:m AND DAY(sa.attend_date)=:d AND sa.ss_class=:c AND sa.member=:sm")
    d = datetime.date(year,month,day)
    result = SabbathSchoolAttend.query.filter_by(attend_date=d,ss_class=sid,member=id).first()
    # result1 = db.engine.execute(result_sql,sm=id,c=sid,y=year,m=month,d=day).fetchone()
    if result:
        print(result)
        db.session.delete(result) 
        db.session.commit()
        flash('The entry was deleted',category='success')
        return redirect(url_for('attendance',id=id,sid=sid,year=year))
    else:
        flash('There was an error handling this request',category='danger')
        return redirect(url_for('attendance',id=id,sid=sid,year=year))





@app.route('/class_attendance/<int:sid>')
@login_required
def class_attendance(sid):
    sschool = SabbathSchool.query.get_or_404(sid)
    result = db.session.query(SabbathSchoolAttend.attend_date, func.count(SabbathSchoolAttend.id)).filter_by(ss_class=sid).group_by(SabbathSchoolAttend.attend_date).order_by(SabbathSchoolAttend.attend_date).all()
    # print(result[0][0])
    attend_dates = []
    attend_count = []
    for r in result:
        attend_dates.append((r[0].strftime('%m/%d/%Y')))
        attend_count.append(r[1])

    return render_template('class_attendance.html',title='Class Attendance',attend_dates=attend_dates,attend_count=attend_count,sschool=sschool)
       



@app.route('/attendance/<int:id>/<int:sid>', methods=['GET', 'POST'])
@app.route('/attendance/<int:id>/<int:sid>/<int:year>/<string:which>', methods=['GET', 'POST'])
@login_required
def attendance(id,sid,year=0,which='default'):
    
    def mSplit(mString):
        m = mString.split()
        return m

    def mNum(mString):
        mDict = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
        return(mDict[mString])


    user = User.query.get_or_404(id)
    sschool = SabbathSchool.query.get_or_404(sid)
    form = AttendanceForm()
    form.ss_class.data = sid
    form.member.data = id
    mnames = "January February March April May June July August September October November December"
    mnames = mnames.split()
    
    # year = request.form["year"]
    if(year == 0):
        today = datetime.datetime.now()
        year = today.year
    # year1, month = time.localtime()[:2]
    else:
        if (which=='prev'):
            year = year - 1
        else:
            year = year + 1

            


    if form.validate_on_submit():
        print(form.ss_class)
        print('Check class variable')
        schoolAttend = SabbathSchoolAttend(ss_class=int(form.ss_class.data),attend_date=form.date.data,member=int(form.member.data))
        db.session.add(schoolAttend)
        db.session.commit()
        flash('The attendance record was successfully updated',category='success')
    else:
        print("FORM DID NOT VALIDATE....................")

    #Creating data for the graph
    old_date = datetime.date(year,1,1)
    new_date = datetime.date.today()
    date_delta = new_date - old_date
    weeks_so_far = round(date_delta.days/7.0)
    total_visits = 0
    mycal = dict() 
    for i in range(12):
        cal = calendar.Calendar(6)
        month_days = cal.itermonthdays(year, (i+1))
        month = []
        count = 1
        for day in month_days:
            if (count % 7 == 0) and (day != 0) :
                attachInfo=""
                attend = SabbathSchoolAttend.query.filter_by(attend_date=datetime.datetime(year,i+1,day),member=id).all()
                if attend:
                    attachInfo = " - PRESENT"
                    total_visits = total_visits + 1
                else:
                    attachInfo = " - ********"
                month.append(str(day)+attachInfo)
            count = count + 1
        mycal[mnames[i]] = month

    return render_template(
            'attendance.html',
            title='Attendance History',
            mycal=mycal,
            year=year,
            mnames=mnames,
            user=user,
            sid=sid,
            sschool=sschool,
            mSplit = mSplit,
            mNum=mNum,
            total_visits=total_visits,
            weeks_so_far = weeks_so_far,
            form=form
            )


@app.route('/detail/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    user = User.query.get_or_404(id)

    departments = db.session.query(Department,MemberDepartment).filter(Department.id==MemberDepartment.department_id,
           MemberDepartment.user_id==user.id).all()


    relatives = db.session.query(Family,User,FamilyRelationship).filter(User.id==FamilyRelationship.family_member,FamilyRelationship.user_id==user.id,Family.id==FamilyRelationship.relationship).all()

    phones = db.session.query(Phone,User).filter(Phone.user_id==User.id,User.id==user.id).all()

    return render_template(
            'detail.html',
            title='User Information',
            user=user,
            departments=departments,
            relatives=relatives,
            phones=phones
            )


@app.route('/editrelative/<int:id>',methods=['GET','POST'])
@login_required
def editrelative(id):
    title = 'Edit Relatives'
    user = User.query.get_or_404(id)
    form = FamilyForm()
    if form.validate_on_submit():
        family = FamilyRelationship(user_id=id,family_member=form.user.data,relationship=form.type.data)
        db.session.add(family)
        db.session.commit()
        flash('Family member successfully added',category='success')
    relatives = db.session.query(Family,User,FamilyRelationship).filter(User.id==FamilyRelationship.family_member,FamilyRelationship.user_id==user.id,Family.id==FamilyRelationship.relationship).all()
    return render_template('editrelative.html',title=title,relatives=relatives,user=user,form=form)



@app.route('/changedeptname/<int:id>',methods=['GET','POST'])
@login_required
def changedeptname(id):
    form = AddDepartmentForm()
    title = 'Change Department Name'
    dept = Department.query.get_or_404(id)
    if form.validate_on_submit():
        dept.dept_name = form.dept_name.data
        db.session.add(dept)
        db.session.commit()
        flash('The Department Name was Successfully Updated',category='success')
        return redirect(url_for('departments'))
    else:
        form.dept_name.data = dept.dept_name

    return render_template('changedeptname.html',title=title,form=form,dept=dept)


@app.route('/changeclassname/<int:id>',methods=['GET','POST'])
@login_required
def changeclassname(id):
    form = SabbathSchoolForm()
    title = 'Change Sabbath School Name'
    ss = SabbathSchool.query.get_or_404(id)
    if form.validate_on_submit():
        ss.name = form.name.data
        db.session.add(ss)
        db.session.commit()
        flash('The Unit Name was Successfully Updated',category='success')
        return redirect(url_for('sschools'))
    else:
        form.name.data = ss.name
    return render_template('changeclassname.html',title=title,form=form,ss=ss)


@app.route('/removefam/<int:id>/<int:fid>',methods=['GET','POST'])
@login_required
def removefam(id,fid):
    fam = FamilyRelationship.query.get_or_404(id)
    db.session.delete(fam)
    db.session.commit()
    flash('Family successfully deleted!',category='success')
    return redirect(url_for('editrelative',id=fid))


@app.route('/removedept/<int:id>/<int:mid>',methods=['GET','POST'])
@login_required
def removedept(id,mid):
    mem = MemberDepartment.query.get_or_404(id)
    db.session.delete(mem)
    db.session.commit()
    flash('Department successfully deleted!',category='success')
    return redirect(url_for('editdepartment',id=mid))

@app.route('/removephone/<int:id>/<int:pid>',methods=['GET','POST'])
@login_required
def removephone(id,pid):
    p = Phone.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Phone # successfully deleted!',category='success')
    return redirect(url_for('editphone',id=pid))



@app.route('/searchusers', methods=['GET'])
def searchusers():
    term = request.args.get('term')
    terms =[]
    html=""
    users = User.query.filter(User.firstname.like('%'+str(term)+'%') |  User.lastname.like('%'+str(term)+'%')      ).limit(10)
    for u in users:
        d = dict()
        d["key"] = u.id
        d["value"] = u.firstname + " " + u.lastname
        d["id"] = u.id
        d["firstname"] = u.firstname
        d["lastname"] = u.lastname 
        # d["email"] = u.email 
        terms.append(d)
    return jsonify(terms) 


@app.route('/editdepartment/<int:id>',methods=['GET','POST'])
@login_required
def editdepartment(id):
    title = 'Edit Department'
    user = User.query.get_or_404(id)
    departments = db.session.query(Department,MemberDepartment).filter(Department.id==MemberDepartment.department_id,
           MemberDepartment.user_id==user.id).all()
    form = DepartmentForm()

    f = request.form.get('dept_name')

    if form.validate_on_submit():
        member_department = MemberDepartment(user_id=user.id,department_id=form.dept_name.data)
        db.session.add(member_department)
        db.session.commit()
        return redirect(url_for('editdepartment',id=user.id))
    return render_template('editdepartment.html',title=title,departments=departments,user=user,form=form)


@app.route('/departments',methods=['GET','POST'])
@login_required
def departments():
    form = AddDepartmentForm()
    title='Departments'
    departments = Department.query.order_by(Department.dept_name).all()
    if form.validate_on_submit():
        dept = Department(dept_name=form.dept_name.data)
        db.session.add(dept)
        db.session.commit()
        flash('Department was added Successfully',category='success')
        return redirect(url_for('departments'))
    return render_template('departments.html',departments=departments,title=title,form=form)



@app.route('/editphone/<int:id>',methods=['GET','POST'])
@login_required
def editphone(id):
    title = 'Edit Phone'
    user = User.query.get_or_404(id)
    form = EditPhoneForm()

    if form.validate_on_submit():
        phone = Phone(user_id=id,phone=form.phone.data,primary_secondary=form.primary_secondary.data,network=form.network.data)
        db.session.add(phone)
        db.session.commit()
        flash('Phone number added successfully', category='success')

    phones = Phone.query.filter_by(user_id=id).all()

    return render_template('editphone.html',title=title,phones=phones,form=form,user=user)


@app.route('/edituser/<int:id>',methods=['GET','POST'])
@login_required
def edituser(id):
    title='Edit User'
    user = User.query.get_or_404(id)
    mypic = user.picture
    if not user:
        abort(404)
    form = EditUserForm()
    if form.validate_on_submit():
        filename = ""
        file = request.files['picture']
        if file:
            print("Debugging*********************************")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename=str(uuid.uuid4())+filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                user.picture = filename
            else:
                flash('Only jpeg, jpg or png files are accepted',category='danger')
                return redirect(url_for('edituser',id=user.id))

        user.email = form.email.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.middlename = form.middlename.data
        user.gender = form.gender.data
        user.dob = form.dob.data
        user.marriage_date = form.marriage_date.data
        user.baptism_date = form.baptism_date.data
        user.marital_status = form.marital_status.data
        user.no_children = form.no_children.data
        user.employment_status = form.employment_status.data
        user.deceased = form.deceased.data
        user.occupation = form.occupation.data
        user.place_of_employment = form.place_of_employment.data
        user.certification = form.certification.data
        user.street = form.street.data
        user.city  = form.city.data
        user.state = form.state.data
        user.zip  = form.zip.data
        db.session.add(user)
        db.session.commit()
        flash('User has been edited',category='success')
        return redirect(url_for('detail',id=user.id))
    else:
        form.email.data = user.email
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.middlename.data = user.middlename
        form.gender.data = user.gender
        form.dob.data = user.dob
        form.marriage_date.data = user.marriage_date
        form.baptism_date.data = user.baptism_date
        form.marital_status.data = user.marital_status
        form.no_children.data = user.no_children
        form.employment_status.data = user.employment_status
        form.deceased.data = user.deceased
        form.occupation.data = user.occupation
        form.place_of_employment.data = user.place_of_employment
        form.certification.data = user.certification
        form.street.data = user.street
        form.city.data = user.city
        form.state.data = user.state
        form.zip.data = user.zip

    return render_template('edituser.html',form=form,title=title,id=user.id,user=user)


@app.route('/adduser',methods=['GET','POST'])
@login_required
def adduser():
    title='Add User'
    #user = User.query.get_or_404(id)
#    mypic = user.picture
#    if not user:
#        abort(404)
    form = AddUserForm()
    if form.validate_on_submit():
        if form.email.data:
            email = User.query.filter_by(email=form.email.data).first()
            if email:
                flash('This email already exists!',category='danger')
                return redirect(url_for('adduser'))

        filename = ""
        file = request.files['picture']
        if file:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename=str(uuid.uuid4())+filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            else:
                flash('Only jpeg, jpg or png files are accepted',category='danger')
                return redirect(url_for('adduser'))
        user = User(
            email = form.email.data,
            firstname = form.firstname.data,
            lastname = form.lastname.data,
            middlename = form.middlename.data,
            gender = form.gender.data,
            dob = form.dob.data,
            marriage_date = form.marriage_date.data,
            baptism_date = form.baptism_date.data,
            marital_status = form.marital_status.data,
            no_children = form.no_children.data,
            picture = filename,
            occupation = form.occupation.data,
            place_of_employment = form.place_of_employment.data,
            certification = form.certification.data,
            street = form.street.data,
            city  = form.city.data,
            state = form.state.data,
            zip  = form.zip.data)
        db.session.add(user)
        db.session.commit()
        flash('User has been Added',category='success')
        return redirect(url_for('detail',id=user.id))
    return render_template('adduser.html',form=form,title=title)



@app.route('/deleteuser/<int:id>',methods=['GET','POST'])
@login_required
def deleteuser(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User successfully deleted!',category='success')
    return redirect(url_for('main'))



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out!', category='success')
    return redirect(url_for('login'))
