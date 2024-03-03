# Login_app Routing
from flask import Blueprint
from flask import render_template, request, redirect
from db_loging import check_login, signupuser, db_password_updated, confirm_email, check_account

# Import library to run the email message
#from flask import current_app
from flask_mail import Mail, Message

from random import randint

#it necessary to check if we can move to main app
from flask_login import login_user

#Define variable to sent email. 
mail = Mail()
# Random OPT code
otp=randint(100000,999999)

#Defining a Blueprint
app_loging = Blueprint('app_loging',__name__)

# Call login and singup html page
@app_loging.route('/login.html')
def login():
  check_loging = 0
  return render_template('/login.html',check_loging=check_loging)

#User enter the login and password
@app_loging.route('/login/apply', methods=['GET', 'POST'])
def login_account():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
      email = request.form['email']
      password = request.form['password']
      login_check = check_login(email,password)
      if login_check == None:
          msg = 'Incorrect login credentials !!!'
          return render_template('/login.html',msg=msg,check_loging=2)
      elif login_check == 'EMAIL_NOT_VALID':
          msg = 'Email is not verified yet, It was sent another email to verify your account!!!'
          msg_email=Message('Cars-Fleet: Email Verification!!!',sender='carsfleetus@gmail.com',recipients=[email])
          #link when we release the version
          #msg_email.body=("Hi Customer, \r\n\r\nPlease click in the link below to confirm your email.\r\n\r\n"+"https://www.cars-fleet.com/email_confirmation/"+email+"\r\n\r\nThanks,\r\nCars-Fleet Team")
          msg_email.body=("Hi Customer, \r\n\r\nPlease click in the link below to confirm your email.\r\n\r\n"+"https://68a735de-441b-4c0b-b492-c780ef1d4274-00-o84d4g0hxvkd.spock.repl.co/email_confirmation/"+email+"\r\n\r\nThanks,\r\nCars-Fleet Team")
          mail.send(msg_email)
          return render_template('/login.html',msg=msg,check_loging=2)
      elif login_check != None:
          login_user(login_check)
          return redirect('/userlogged')

@app_loging.route('/signup/apply',methods=['GET', 'POST'])
def signupaccount():
  data = request.form
  email=data['email']
  result = signupuser(data)
  if result == "USER_EXISTE":
    msg="Email already used"
    return render_template('/login.html',msg=msg,check_loging=2)
  else:
    #Verify Registraction by email.
    msg="Please verify your email address!!!"
    msg_email=Message('Cars-Fleet: Email Verification!!!',sender='carsfleetus@gmail.com',recipients=[email])

    #Release Version
    #msg_email.body=("Hi Customer, \r\n\r\nPlease click in the link below to confirm your email.\r\n\r\n"+"https://www.cars-fleet.com/email_confirmation/"+email+"\r\n\r\nThanks,\r\nCars-Fleet Team")
    #Replit verion
    msg_email.body=("Hi Customer, \r\n\r\nPlease click in the link below to confirm your email.\r\n\r\n"+"https://68a735de-441b-4c0b-b492-c780ef1d4274-00-o84d4g0hxvkd.spock.repl.co/email_confirmation/"+email+"\r\n\r\nThanks,\r\nCars-Fleet Team")
    mail.send(msg_email)
    return render_template('/login.html',msg=msg,check_loging=3)

# Password Reset
@app_loging.route('/verify',methods=['POST'])
def verify():
  email=request.form['email']
  account_exist = check_account(email)
  if account_exist == "USER_EXISTE":
    msg=Message('Cars-Fleet: Password Reset!!!',sender='carsfleetus@gmail.com',recipients=[email])
    msg.body=("Hi Customer, \r\n\r\n This is an automatic menssage to validate your password.\r\n\r\nCode: " + str(otp))
    mail.send(msg)
    return render_template('reset_password.html',check_reset=2,email=email)
  else:
    msg="No user founded, please signup"
    return render_template('/login.html',msg=msg,check_loging=3)

@app_loging.route('/validate',methods=['POST'])
def validate():
  data = request.form
  #print(data)
  user_otp=request.form['OTP_code']
  if otp==int(user_otp):
    db_password_updated(data)
    return "<h2>Password update/h2>"
  else:
    return "<h2>Verification failed otp does not match</h2>"

@app_loging.route('/reset_password')
def passwrod_reset():
  return render_template('/reset_password.html',check_reset=0)

@app_loging.route('/email_confirmation/<emailaddress>')
def email_confirmation(emailaddress):
  confirm_email(emailaddress)
  return "<h2>Email Verification</h2>"