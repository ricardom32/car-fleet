from flask import Blueprint
from flask import render_template, request
from flask_login import login_required
from db_account import db_new_account, db_customer_search ,detail_account, edit_user, db_customer_updated

#Defining a Blueprint
app_customer = Blueprint('app_customer',__name__)

# Customer Information
@app_customer.route('/forms/customer')
@login_required
def new_account():
  return render_template('/form_customer.html',tab_id="1")

@app_customer.route('/forms/new_account/apply',methods=['GET', 'POST'])
@login_required
def customer_account():
  data = request.form.to_dict()
  #Use to upload license's drive to dababase
  uploaded_file = request.files["photo"]
  if uploaded_file.filename != "": 
      uploaded_file.save("static/photo_id_1.png") 
  with open('static/photo_id_1.png', 'rb') as file:
    binaryData = file.read()
  data['photo'] = binaryData
  db_new_account(data) 
  return 'New Register updated'

@app_customer.route('/forms/customer_search/apply',methods=['GET', 'POST'])
@login_required
def customer_search():
  search_customer = request.form
  if len(search_customer) <= 3 or search_customer['search'] == "" :
    return render_template('/customer_form.html',search_customer="",tab_id="2")
  else:
    result_search = db_customer_search(search_customer)
    if db_customer_search(search_customer) == None:
        return render_template('/form_customer.html',search_customer="",tab_id="2")
    else:
      search_customer=result_search
      return render_template('/form_customer.html',search_customer=search_customer,tab_id="2")

@app_customer.route('/forms/account_detail/<id>')
@login_required
def account_detail(id):
  searched_account=detail_account(id)
  binary_data = searched_account['photo']
  with open('static/photo_id_2.png', 'wb') as file:
    file.write(binary_data)
  return render_template('/form_customer.html',searched_account=searched_account,tab_id="3")

@app_customer.route('/forms/new_account/edit')
@login_required
def account_edit():
  user_edit=edit_user()
  return render_template('/form_customer.html',user_edit=user_edit,tab_id="4")

@app_customer.route('/forms/new_account/updated',methods=['GET', 'POST'])
@login_required
def customer_updated():
  #data = request.form
  data = request.form.to_dict()
  #Use to upload license's drive to dababase
  uploaded_file = request.files["photo"]
  #Convert digital data to binary format
  if uploaded_file.filename != "": 
      uploaded_file.save("static/photo_id_1.png") 
  with open('static/photo_id_1.png', 'rb') as file:
    binaryData = file.read()
  data['photo'] = binaryData
  db_customer_updated(data) 
  return 'Usuario Atualizado'