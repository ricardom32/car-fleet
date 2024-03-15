from sqlalchemy import create_engine, text
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

# Class for itentify user
from User import User

#my_secret = os.environ['DB_CARFLEET']
my_secret = os.environ['DB_CARS-FLEET_AIVEN']
engine =create_engine(my_secret,connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}}, isolation_level="AUTOCOMMIT")

# Check the Login
def check_login(email, password):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts_admin WHERE email = :email"), dict(email=email))
    user = result.fetchone()
    if not user:
      return None

    # load the user information to user 
    print(result)
    user = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[16], user[17], user[18], user[19], user[20], user[21], user[22], user[23], user[24], user[25], user[26], user[27], user[28], user[29], user[30], user[31], user[32], user[33], user[34], user[35], user[36], user[37],user[38])

    passwrod_db = user.password
    valid_email = user.valid

    if check_password_hash (passwrod_db, password) and valid_email == "YES":
      return user
    elif check_password_hash(passwrod_db, password) and valid_email == "NO":
      return "EMAIL_NOT_VALID"
    else:
      return None

# link the user for longing
def get_user_by_id(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts_admin WHERE id = :id"), dict(id=id))
    user = result.fetchone()  
    if user != None:
      logged_user = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[16], user[17], user[18], user[19], user[20], user[21], user[22], user[23], user[24], user[25], user[26], user[27], user[28], user[29], user[30], user[31], user[32], user[33], user[34], user[35], user[36], user[37],user[38])
      #Arquive the user in session
      session["id"] = logged_user.id
      session["email_admin"] = logged_user.email_admin
      session["branch"] = logged_user.branch
      session["email"] = logged_user.email
      session["reservation_main"] = logged_user.reservation_main
      session["reservation_reg"] = logged_user.reservation_reg
      session["reservation_detail"] = logged_user.reservation_detail
      session["customer_main"] = logged_user.customer_main
      session["customer_reg"] = logged_user.customer_reg
      session["customer_detail"] = logged_user.customer_detail
      session["maintenance_main"] = logged_user.maintenance_main
      session["maintenance_reg"] = logged_user.maintenance_reg
      session["maintenance_detail"] = logged_user.maintenance_detail
      session["car_main"] = logged_user.car_main
      session["car_reg"] = logged_user.car_reg
      session["car_detail"] = logged_user.car_detail
      session["team_main"] = logged_user.team_main
      session["team_reg"] = logged_user.team_reg
      session["team_detail"] = logged_user.team_detail
      session["employee_main"] = logged_user.employee_main
      session["employee_reg"] = logged_user.employee_reg
      session["employee_detail"] = logged_user.employee_detail
      session["expenses_main"] = logged_user.expenses_main
      session["expenses_reg"] = logged_user.expenses_reg
      session["expenses_detail"] = logged_user.expenses_detail
      session["view_plan"] = logged_user.view_plan
 
      return logged_user
    else:
      return None

# User Register in the Database Accounts.
def signupuser(data):
  email = data['email']
  password = data['password']
  password = generate_password_hash(password)
  user_add = {"email_admin":email, "password_admin": password, "email": email, "password": password, "valid": 'NO'}

  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts_admin WHERE email = :email"), dict(email=email))

  if len(result.all())!=0:
    return "USER_EXISTE"
  else:  
    with engine.connect() as conn:
      query = text("INSERT INTO accounts_admin (email_admin, email, password, valid) VALUES (:email_admin, :email, :password, :valid)")
      conn.execute(query, user_add)
    return "SIGNEDUP"

def db_password_updated(data):
  email = data['email']
  password = data['new_password']
  valid = "YES"
  password = generate_password_hash(password)
  new_password = {"email_admin":email, "email": email, "password": password, "valid": valid}
  with engine.connect() as conn:
    query = text("UPDATE accounts_admin SET password = :password WHERE email =:email")
    conn.execute(query,new_password)

#Confirm the user by email verification
def confirm_email(emailaddress):
  email = {"email": emailaddress}
  valid = {"email": emailaddress, "password": 'N/A', "valid": 'YES'}
  print(email)
  with engine.connect() as conn:
    query = text("UPDATE accounts_admin SET valid= :valid WHERE email =:email")
    conn.execute(query,valid)
    return "Email_Confirmed"

# Check if the material exist for reset password
def check_account(email):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts_admin WHERE email = :email"), dict(email=email))
  if len(result.all())!=0:
    return "USER_EXISTE"
  else:  
    return "NO_USER"