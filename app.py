from flask import Flask, render_template, request, redirect
from db_loging import login_check1, signupuser, get_user_by_id
#from db_account import db_new_account, db_customer_search ,detail_account, edit_user, db_customer_updated
#from db_car import car_register,db_car_search ,detail_car, edit_car, db_car_updated

from app_car import app_car
from app_customer import app_customer

# project the access the database with Token
from flask_wtf.csrf import CSRFProtect

# login
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.register_blueprint(app_car)
app.register_blueprint(app_customer)
#app.register_blueprint(app_login)

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
  return render_template('/sidebar.html')

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
'''
# Customer Information
@app.route('/forms/customer_new')
@login_required
def new_account():
  return render_template('/customer_form.html',tab_id="1")

@app.route('/forms/new_account/apply',methods=['GET', 'POST'])
@login_required
def customer_account():
  data = request.form
  db_new_account(data) 
  return 'New Register updated'

@app.route('/forms/customer_search/apply',methods=['GET', 'POST'])
@login_required
def customer_search():
  search_customer = request.form
  if len(search_customer) <= 3 or search_customer['search'] == "" :
    return render_template('/customer_form.html',search_customer="",tab_id="2")
  else:
    result_search = db_customer_search(search_customer)
    if db_customer_search(search_customer) == None:
        return render_template('/customer_form.html',search_customer="",tab_id="2")
    else:
      search_customer=result_search
      return render_template('/customer_form.html',search_customer=search_customer,tab_id="2")

@app.route('/forms/account_detail/<id>')
@login_required
def account_detail(id):
  searched_account=detail_account(id)
  return render_template('/customer_form.html',searched_account=searched_account,tab_id="3")

@app.route('/forms/new_account/edit')
@login_required
def account_edit():
  user_edit=edit_user()
  return render_template('/customer_form.html',user_edit=user_edit,tab_id="4")

@app.route('/forms/new_account/updated',methods=['GET', 'POST'])
@login_required
def customer_updated():
  data = request.form
  db_customer_updated(data) 
  return 'Usuario Atualizado'

# Car Information
@app.route('/forms/car_form')
@login_required
def car_registration():
  return render_template('/car_reg_form.html',tab_id="1")

@app.route('/forms/car_register/apply',methods=['GET', 'POST'])
@login_required
def db_car_register():
  data = request.form
  car_register(data) 
  return 'New Register updated'

@app.route('/forms/car_search/apply',methods=['GET', 'POST'])
@login_required
def car_search():
  search_customer = request.form
  print(search_customer)
  print(len(search_customer))
  if len(search_customer) <= 3 or search_customer['search'] == "" :
    print("1")
    return render_template('/car_reg_form.html',search_customer="",tab_id="2")
  else:
    print("2")
    result_search = db_car_search(search_customer)
    if db_car_search(search_customer) == None:
      print("3")
      return render_template('/car_reg_form.html',search_customer="",tab_id="2")
    else:
      print("4")
      search_customer=result_search
      print(search_customer)
      return render_template('/car_reg_form.html',search_customer=search_customer,tab_id="2")

@app.route('/forms/car_detail/<id>')
@login_required
def car_detail(id):
  searched_account=detail_car(id)
  return render_template('/car_reg_form.html',searched_account=searched_account,tab_id="3")

@app.route('/forms/new_car/edit')
@login_required
def car_edit():
  user_car=edit_car()
  return render_template('/car_reg_form.html',user_car=user_car,tab_id="4")

@app.route('/forms/new_car/updated',methods=['GET', 'POST'])
@login_required
def car_updated():
  data = request.form
  db_car_updated(data) 
  return 'Usuario Atualizado'
'''
# This call the price table
@app.route('/price_table')
def upload_dl():
  return  render_template('/price_table.html') 

if __name__ == "__main__":
  csrf.init_app(app)
  app.run(host='0.0.0.0', debug=True)