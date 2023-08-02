from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import car_inf_db, cars_inf_db, add_car_reg_db, login_check1, signupuser, get_user_by_id
from flask_sqlalchemy import SQLAlchemy

from werkzeug.datastructures import ImmutableMultiDict

# project the access the database with Token
from flask_wtf.csrf import CSRFProtect

# login
from flask_login import LoginManager, login_user, logout_user, login_required

#Import class User to identify the longin
from User import User

app = Flask(__name__)
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)
app.config['SECRET_KEY'] = 'thisisasecretkeyforcarfleet'

#user_by_id = User(2, 'ricardom32', 'Rgtmri930#1', 'ricardom32@hotmail.com')
#user_by_id = User(1, 'ricardo', 'Rgtmri930#1', 'ricardom32@hotmail.com')

#itentify the user
@login_manager_app.user_loader
def load_user(id):
  return get_user_by_id(id)
  #return user_by_id

@app.route("/")
def Car_easy_fleet():
  car_inf = car_inf_db()
  return render_template('home.html', car_inf=car_inf, company_name='Car Fleet')

@app.route("/api/car_inf/<id>")
def list_car_inf(id):
  car_inf=cars_inf_db(id)
  return jsonify(car_inf)

@app.route('/dashboard/<id>')
def dashboard(id):
  dashboard = cars_inf_db(id)
  return render_template('dashboard.html',dashboard=dashboard)

@app.route("/car_inf/<id>/apply", methods=["post"])
def apply_to_car(id):
  data = request.form
  add_car_reg_db(data)
  return render_template('car_reg_submit.html',car_reg=data)

@app.route('/login.html')
def login():
  return render_template('/login.html')

@app.route('/login/apply', methods=['GET', 'POST'])
def login_account():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
      username = request.form['username']
      password = request.form['password']
      login_check = login_check1(username,password)
      if login_check != None:
        login_user(login_check)
        return render_template('/vertbarcode.html')
      else:
        return 'Error 505'
        
#      if login_check == 'user_loggedin':
#        login_user(user_by_id)
#        return render_template('/vertbarcode.html')
#      else:
#        return 'Error 505'

@app.route('/protected.html')
@login_required
def protected():
  return "<h1>Esta pagina esta protegida, solo usuario autorizaod puedes accessar."

@app.route('/logout.html')
def logout():
  logout_user()
  return "<h1>Logout done. </h1>"

@app.route('/signup.html')
def signup():
  return render_template('/signup.html')

@app.route('/signup/apply',methods=['GET', 'POST'])
def signupaccount():
  data = request.form
  #password = request.form['password']
  #email = request.form['email']
  #data = [username, password, email]
  #print(data)
  signupuser(data) 
  return 'Usuario Registrado'

if __name__ == "__main__":
  csrf.init_app(app)
  app.run(host='0.0.0.0', debug=True)
