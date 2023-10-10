from flask import Blueprint
from flask import Flask, render_template, request, redirect
from db_loging import login_check1, signupuser, get_user_by_id
from flask import render_template, request
from flask_login import login_required

# login
from flask_login import LoginManager, login_user, logout_user, login_required

#Defining a Blueprint
app_loging = Blueprint('app_loging',__name__)

#itentify the user
@login_manager_app.user_loader
def load_user(id):
  return get_user_by_id(id)

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
      login_check = login_check1(email,password)
      if login_check != None:
        login_user(login_check)
        return redirect('/userlogged')
      else:
        msg = 'Incorrect login credentials !!!'
        return render_template('/login.html',msg=msg,check_loging=2)

#Open the page with logged user
@app_loging.route('/userlogged')
@login_required
def user_loged():
  return render_template('/sidebar.html')

@app_loging.route('/signup/apply',methods=['GET', 'POST'])
def signupaccount():
  data = request.form
  result = signupuser(data)
  if result == "USER_EXISTE":
    msg="Email already used"
    return render_template('/login.html',msg=msg,check_loging=2)
  else:
    msg="User Registrated, Please logned in."
    return render_template('/login.html',msg=msg,check_loging=3)

@app_loging.route('/logout')
def logout():
  logout_user()
  return render_template('/home.html')
