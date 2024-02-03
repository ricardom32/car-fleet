# Car_app Routing
from flask import Blueprint
from flask import render_template, request
from flask_login import login_required
from db_car import car_register,db_car_search ,detail_car, edit_car, db_car_updated

#Defining a Blueprint
app_expense = Blueprint('app_expense',__name__)

# Car Information
@app_expense.route('/forms/expense')
@login_required
def car_registration():
  return render_template('/form_expense.html',tab_id="1")

@app_expense.route('/forms/maintenance_reg/apply',methods=['GET', 'POST'])
@login_required
def db_car_register():
  data = request.form
  car_register(data) 
  return 'New Register updated'

@app_expense.route('/forms/maintenance_search/apply',methods=['GET', 'POST'])
@login_required
def car_search():
  search_customer = request.form
  print(search_customer)
  print(len(search_customer))
  if len(search_customer) <= 3 or search_customer['search'] == "" :
    print("1")
    return render_template('/form_maintenance.html',search_customer="",tab_id="2")
  else:
    print("2")
    result_search = db_car_search(search_customer)
    if db_car_search(search_customer) == None:
      print("3")
      return render_template('/form_maintenance.html',search_customer="",tab_id="2")
    else:
      print("4")
      search_customer=result_search
      print(search_customer)
      return render_template('/form_maintenance.html',search_customer=search_customer,tab_id="2")

@app_expense.route('/forms/car_detail/<id>')
@login_required
def car_detail(id):
  searched_account=detail_car(id)
  return render_template('/form_maintenance.html',searched_account=searched_account,tab_id="3")

@app_expense.route('/forms/new_maintenance/edit')
@login_required
def car_edit():
  user_car=edit_car()
  return render_template('/car_reg_form.html',user_car=user_car,tab_id="4")

@app_expense.route('/forms/new_maintenance/updated',methods=['GET', 'POST'])
@login_required
def car_updated():
  data = request.form
  db_car_updated(data) 
  return 'Usuario Atualizado'
