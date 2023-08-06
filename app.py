from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import car_inf_db, cars_inf_db, add_car_reg_db, login_check1, signupuser, get_user_by_id

# project the access the database with Token
from flask_wtf.csrf import CSRFProtect

# login
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)
app.config['SECRET_KEY'] = 'thisisasecretkeyforcarfleet'

#itentify the user
@login_manager_app.user_loader
def load_user(id):
  return get_user_by_id(id)

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
        return render_template('/sidebar.html')
      else:
        return 'Error 505'

@app.route('/protected.html')
@login_required
def protected():
  return "<h1>Esta pagina esta protegida, solo usuario autorizaod puedes accessar."

@app.route('/logout')
def logout():
  logout_user()
  return render_template('home.html')

@app.route('/signup.html')
def signup():
  return render_template('/signup.html')

@app.route('/signup/apply',methods=['GET', 'POST'])
def signupaccount():
  data = request.form
  signupuser(data) 
  return 'Usuario Registrado'

@app.route('/sidebar')
def sidebar():
  return render_template('/sidebar.html')

@app.route('/useraccount')
def teste():
  return render_template('/useraccount.html')

@app.route('/customer_reg')
def customer_reg():
  return render_template('/customer_reg.html')

if __name__ == "__main__":
  csrf.init_app(app)
  app.run(host='0.0.0.0', debug=True)