from flask import Blueprint
from flask import render_template, request, session
from flask_login import login_required
from db_branches import db_new_team, db_customer_search ,detail_account, edit_user, db_customer_updated

from flask import current_app
from flask_mail import Mail, Message
import secrets

#Defining a Blueprint
app_branches = Blueprint('app_branches',__name__)

# Customer Information
@app_branches.route('/forms/team')
@login_required
def new_team():
  return render_template('/form_branches.html',tab_id="1")

@app_branches.route('/forms/new_team/apply',methods=['GET', 'POST'])
@login_required
def team_account():
  data = request.form.to_dict()
  #create password for the team user
  password_length = 13
  data['password'] = secrets.token_urlsafe(password_length)
  data['password_admin'] = secrets.token_urlsafe(password_length)
  provistion_password = data['password']
  #copy the user in the email_admin.
  data['email_admin'] = session["email"]

  #db_new_team(data) 
  new_team = db_new_team(data)
  if new_team == "USER_EXISTE":
    return "User already exist, please use another email!!!"
  else:
    with current_app.app_context():
      #retun the email that new team user was created.
      email = new_team
      msg = 'Email is not verified yet, It was sent another email to verify your account!!!'
      msg_email=Message('Cars-Fleet: Email Verification!!!',sender='carsfleetus@gmail.com',recipients=[email])
      msg_email.body=("Hi Customer, \r\n\r\nPlease click in the link below to confirm your email.\r\n\r\n"+"Provisinal Password:  "+provistion_password+"\r\n\r\nThanks,\r\nCars-Fleet Team")
      mail = Mail()
      mail.send(msg_email)
    return 'New Register updated'

@app_team.route('/forms/customer_search/apply',methods=['GET', 'POST'])
@login_required
def customer_search():
  search_customer = request.form
  if len(search_customer) <= 3 or search_customer['search'] == "" :
    return render_template('/form_customer.html',search_customer="",tab_id="2")
  else:
    result_search = db_customer_search(search_customer)
    if db_customer_search(search_customer) == None:
        return render_template('/form_customer.html',search_customer="",tab_id="2")
    else:
      search_customer=result_search
      return render_template('/form_customer.html',search_customer=search_customer,tab_id="2")

@app_branches.route('/forms/account_detail/<id>')
@login_required
def account_detail(id):
  searched_account=detail_account(id)
  binary_data = searched_account['photo']
  with open('static/photo_id_2.png', 'wb') as file:
    file.write(binary_data)
  return render_template('/form_customer.html',searched_account=searched_account,tab_id="3")

@app_branches.route('/forms/new_account/edit')
@login_required
def account_edit():
  user_edit=edit_user()
  return render_template('/form_customer.html',user_edit=user_edit,tab_id="4")

@app_branches.route('/forms/new_account/updated',methods=['GET', 'POST'])
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