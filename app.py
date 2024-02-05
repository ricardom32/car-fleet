from flask import Flask, render_template, request, redirect
from db_loging import login_check1, signupuser, get_user_by_id

# import password liberies
from flask import*
from flask_mail import*
from random import*
import ssl

#Blueprint library
from app_car import app_car
from app_customer import app_customer
from app_maintenance import app_maintenance
from app_reservation import app_reservation
from app_employee import app_employee
from app_expense import app_expense
from app_dashboard import app_dashboard

# project the access the database with Token
from flask_wtf.csrf import CSRFProtect

# login
from flask_login import LoginManager, login_user, logout_user, login_required

# import modules Flask and Bluprints
app = Flask(__name__)
app.register_blueprint(app_car)
app.register_blueprint(app_customer)
app.register_blueprint(app_maintenance)
app.register_blueprint(app_reservation)
app.register_blueprint(app_employee)
app.register_blueprint(app_expense)
app.register_blueprint(app_dashboard)

#google SMTP server
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='carsfleetus@gmail.com'
app.config['MAIL_PASSWORD']='shhi aepu vibk bbpa'
#app.config['MAIL_PASSWORD']='gzlf bgcz mlpz aady'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
otp=randint(100000,999999)

csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)
app.config['SECRET_KEY'] = 'thisisasecretkeyforcarfleet'

#itentify the user
@login_manager_app.user_loader
def load_user(id):
  return get_user_by_id(id)

@app.route("/")
def Car_easy_fleet():
  return render_template('home.html', company_name='Car Fleet')


# Call login and singup html page
@app.route('/login.html')
def login():
  check_loging = 0
  return render_template('/login.html',check_loging=check_loging)

#User enter the login and password
@app.route('/login/apply', methods=['GET', 'POST'])
def login_account():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
      email = request.form['email']
      password = request.form['password']
      login_check = login_check1(email,password)
      if login_check != None:
        login_user(login_check)
        return redirect('/userlogged')
      else:
        msg = 'Incorrect login credentials !!!'
        return render_template('/login.html',msg=msg,check_loging=2)

#Open the page with logged user
@app.route('/userlogged')
@login_required
def user_loged():
  return render_template('/form_dashboard.html')

@app.route('/signup/apply',methods=['GET', 'POST'])
def signupaccount():
  data = request.form
  result = signupuser(data)
  if result == "USER_EXISTE":
    msg="Email already used"
    return render_template('/login.html',msg=msg,check_loging=2)
  else:
    msg="User Registrated, Please logned in."
    return render_template('/login.html',msg=msg,check_loging=3)

@app.route('/logout')
def logout():
  logout_user()
  return render_template('/home.html')

# This call the price table
@app.route('/price_table')
def upload_dl():
  return  render_template('/price_table.html') 

# Password Rest
@app.route('/verify',methods=['POST'])
def verify():
  email=request.form['email']
  msg=Message('Password Reset Request',sender='carsfleetus@gmail.com',recipients=[email])
  msg.body=str(otp)
  mail.send(msg)
  return render_template('reset_password.html',check_reset=2)

@app.route('/validate',methods=['POST'])
def validate():
  user_otp=request.form['otp']
  if otp==int(user_otp):
    return "<h2>Email verification is successful</h2>"
  else:
    return "<h2>Verification failed otp does not match</h2>"

@app.route('/reset_password')
def passwrod_reset():
  return render_template('/reset_password.html',check_reset=0)

if __name__ == "__main__":
  csrf.init_app(app)
  app.run(host='0.0.0.0', debug=True)