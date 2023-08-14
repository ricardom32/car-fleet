from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import car_inf_db, cars_inf_db, add_car_reg_db, login_check1, signupuser, get_user_by_id, db_new_account

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

@app.route('/forms/customer_new')
def new_account():
  return render_template('/forms/customer/customer_form_new.html')

@app.route('/forms/new_account/apply',methods=['GET', 'POST'])
def customer_account():
  data = request.form
  db_new_account(data) 
  return 'Usuario Registrado'

@app.route('/forms/customer_search')
def customer_search():
  return render_template('/forms/customer/customer_form_search.html')

@app.route('/forms/customer_view')
def customer_inf():
  return render_template('/forms/customer/customer_form_view.html')

"""
@app.route('/forms/dashboard')
def dashboard1():
  return render_template('/forms/dashboard.html')

@app.route('/forms/car_form')
def revenue():
  return render_template('/guidances/form_template.html')

@app.route('/forms/customer_forms')
def customer():
  return render_template('/guidances/form_template.html')

@app.route('/forms/maintenance_form')
def maintenance():
  return render_template('/forms/maintenance_form.html')
  
@app.route('/forms/car_form')
def car():
 return render_template('/forms/car_form.html')

@app.route('/forms/employee_form')
def employee():
  return render_template('crossbar_test.html')

@app.route('/homes')
def news():
  return render_template('/forms/employee_form.html')

@app.route('/news')
def contact():
  return render_template('/forms/revenue.html')
"""

if __name__ == "__main__":
  csrf.init_app(app)
  app.run(host='0.0.0.0', debug=True)