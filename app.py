from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from database import car_inf_db, cars_inf_db, add_car_reg_db, login_check1, signupuser, get_user_by_id
from db_account import db_new_account, db_customer_search,detail_account,edit_user,db_customer_updated
import flash

from werkzeug.datastructures import ImmutableMultiDict

# project the access the database with Token
from flask_wtf.csrf import CSRFProtect

# login
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)
app.config['SECRET_KEY'] = 'thisisasecretkeyforcarfleet'

# Config used to upload the file
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

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

# Call login and singup html page
@app.route('/login.html')
def login():
  check_loging = 0
  return render_template('/login2.html',check_loging=check_loging)

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
        msg = 'Incorrect login credentials !!!'
        return render_template('/login2.html',msg=msg,check_loging=1)

@app.route('/protected.html')
@login_required
def protected():
  return "Esta pagina esta protegida, solo usuario autorizaod puedes accessar."

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
  return render_template('/forms/customer/customer_form_new.html',tab_id="1")

@app.route('/forms/new_account/apply',methods=['GET', 'POST'])
def customer_account():
  data = request.form
  db_new_account(data) 
  return 'Usuario Registrado'

@app.route('/forms/customer_search/apply',methods=['GET', 'POST'])
def customer_search():
  search_customer = request.form
  if len(search_customer) <= 2 or search_customer['search'] == "":
    return render_template('/forms/customer/customer_form_new.html',search_customer="",tab_id="2")
  else:
    result_search = db_customer_search(search_customer)
    if db_customer_search(search_customer) == None:
        return render_template('/forms/customer/customer_form_new.html',search_customer="",tab_id="2")
    else:
      search_customer=result_search
      return render_template('/forms/customer/customer_form_new.html',search_customer=search_customer,tab_id="2")

@app.route('/forms/account_detail/<id>')
def account_detail(id):
  searched_account=detail_account(id)
  return render_template('/forms/customer/customer_form_new.html',searched_account=searched_account,tab_id="3")

@app.route('/forms/new_account/edit')
def account_edit():
  user_edit=edit_user()
  return render_template('/forms/customer/customer_form_new.html',user_edit=user_edit,tab_id="4")

@app.route('/forms/new_account/updated',methods=['GET', 'POST'])
def customer_updated():
  data = request.form
  db_customer_updated(data) 
  return 'Usuario Atualizado'

@app.route('/forms/customer_search/image',methods=['GET', 'POST'])
def upload_dl():
  data = request.form
  db_customer_updated(data) 
  return 'Usuario Atualizado'

@app.route('/forms/file_upload')
def uploadfile():
  return render_template('/forms/customer/meu_test.html')

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