from flask import Blueprint
from flask import render_template, request
from flask_login import login_required
from db_profile import detail_account, edit_user, db_customer_updated

#Defining a Blueprint
app_profile = Blueprint('app_profile',__name__)

# Customer Information
@app_profile.route('/forms/profile')
@login_required
def user_profile():
  return render_template('/form_profile.html',tab_id="1")

@app_profile.route('/forms/profile_detail/<id>')
@login_required
def account_detail(id):
  searched_account=detail_account(id)
  binary_data = searched_account['photo']
  with open('static/photo_id_2.png', 'wb') as file:
    file.write(binary_data)
  return render_template('/form_customer.html',searched_account=searched_account,tab_id="3")

@app_profile.route('/forms/new_profile/edit')
@login_required
def account_edit():
  user_edit=edit_user()
  return render_template('/form_customer.html',user_edit=user_edit,tab_id="4")

@app_profile.route('/forms/new_profile/updated',methods=['GET', 'POST'])
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