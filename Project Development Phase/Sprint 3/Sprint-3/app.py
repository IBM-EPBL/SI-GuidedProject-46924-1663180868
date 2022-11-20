from flask import Flask,render_template,request,url_for,flash,redirect,session
import ibm_db
import sendgrid
import re
from sendgrid.helpers.mail import *
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = Flask(__name__)
app.secret_key="12345"

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wfx06822;PWD=QWFpj7PZhFqXKq2B",'','')

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/home")
def home_page():
    return render_template('home.html')
#------------------------------------------------------

@app.route("/login",methods = ['POST', 'GET'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM LOGIN WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            return render_template('user_profile.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

#---------------------------------------------------------

@app.route('/afterlogin')
def afterlogin():
    return render_template("user_profile.html")

#-------------------------------------------------------

@app.route("/signin",methods = ['POST', 'GET'])
def signin():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        usermail = request.form['usermail']
        usercontact = request.form['usercontact']
        password = request.form['password']
        sql = "SELECT * FROM LOGIN WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', usermail):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            mailtest_registration(usermail)
            insert_sql = "INSERT INTO LOGIN VALUES (?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, usermail)
            ibm_db.bind_param(prep_stmt, 3, usercontact)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('signin.html', msg = msg)
#-------------------------------------------------------------------
# sendgrid integration
def mailtest_registration(to_email):
    message = Mail(
    from_email='rushal1218prem@gmail.com',
    to_emails= to_email,
    subject='Registration Successfull!',
    html_content='<strong>You have successfully registered as user. Please Login using your Username and Password to donate/request for Plasma.</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

#for donor
def mailtest_donor(to_email):
    message = Mail(
    from_email='rushal1218prem@gmail.com',
    to_emails= to_email,
    subject='Thankyou for Registering as Donor!',
    html_content='<strong>Every donor is an asset to the nation who saves peoples lives, and you are one of them.We appreciate your efforts. Thank you!!</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

#for request
def mailtest_request(to_email):
    message = Mail(
    from_email='rushal1218prem@gmail.com',
    to_emails= to_email,
    subject='Request Submitted!',
    html_content='<strong>Your request has been successfully submitted. Please be patient, your requested donor will get back to you soon.</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

#for request sending to donor
def mailtest_requesttodonor(to_email):
    message = Mail(
    from_email='rushal1218prem@gmail.com',
    to_emails= to_email,
    subject='Requesting Plasma',
    html_content='<strong>Your registration has been requested by a recipient, we will share futher details in future. Stay connected!!</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
#-------------------------------------------------------------------------------
@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/adddonor",methods = ['POST','GET'])
def adddonor():
    
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        blood = request.form['blood']
        area = request.form['area']
        city = request.form['city']
        district = request.form['district']

        sql = "SELECT * FROM DONOR2 WHERE name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('donor.html', msg="You are already a member, please login using your details")
        else:
            mailtest_donor(email)
            insert_sql = "INSERT INTO DONOR2 VALUES (?,?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, mobile)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, age)
            ibm_db.bind_param(prep_stmt, 5, gender)
            ibm_db.bind_param(prep_stmt, 6, blood)
            ibm_db.bind_param(prep_stmt, 7, area)
            ibm_db.bind_param(prep_stmt, 8, city)
            ibm_db.bind_param(prep_stmt, 9, district)
            ibm_db.execute(prep_stmt)
        return render_template('success.html', msg="Registered successfuly..")
#-----------------------------------------------------------------------------------------

@app.route('/donorlist')
def donorlist():
    donor2 = []
    sql = "SELECT * FROM DONOR2"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        donor2.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    if donor2:
        return render_template("donor.html", donor2 = donor2)

#----------------------------------------------------------------------------
@app.route("/request_page", methods = ['GET','POST'])
def request_page():
    msg = ''
    if request.method == 'POST' :
        drmail = request.form['drmail']
        hospitalname = request.form['hospitalname']
        recname = request.form['recname']
        recmobile = request.form['recmobile']
        recmail = request.form['recmail']
        recage = request.form['recage']
        recgender = request.form['recgender']
        recbloodgroup = request.form['recbloodgroup']
        recarea = request.form['recarea']
        reccity = request.form['reccity']
        recdistrict = request.form['recdistrict']
        sql = "SELECT * FROM REQUEST2 WHERE recname =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,recname)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Request already exists !'
        else:
            
            mailtest_requesttodonor(drmail)
            insert_sql = "INSERT INTO REQUEST2 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, drmail)
            ibm_db.bind_param(prep_stmt, 2, hospitalname)
            ibm_db.bind_param(prep_stmt, 3, recname)
            ibm_db.bind_param(prep_stmt, 4, recmobile)
            ibm_db.bind_param(prep_stmt, 5, recmail)
            ibm_db.bind_param(prep_stmt, 6, recage)
            ibm_db.bind_param(prep_stmt, 7, recgender)
            ibm_db.bind_param(prep_stmt, 8, recbloodgroup)
            ibm_db.bind_param(prep_stmt, 9, recarea)
            ibm_db.bind_param(prep_stmt, 10, reccity)
            ibm_db.bind_param(prep_stmt, 11, recdistrict)
            ibm_db.execute(prep_stmt)
            msg = 'Your request has been submitted!'
            return render_template('request.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('request.html', msg = msg)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
