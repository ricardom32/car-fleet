from sqlalchemy import create_engine, text
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

# Class for itentify user
from User import User

my_secret = os.environ['DB_CARFLEET']

engine =create_engine(my_secret,connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}})

# Check the Login
def check_login(email, password):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts_admin WHERE email = :email"), dict(email=email))
    user = result.fetchone()
    if not user:
      return None
    # Check the email is validated, by checking the link in the email.
    check_email = user[15]
    # load the user information to user 
    user = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6])
    #user = User(user[0], user[1], user[2], user[3], user[4], user[5], user[16],user[17],user[18],user[19],user[20],user[21],user[22],user[23],user[16], )
    passwrod_db = user.password

    if check_password_hash(passwrod_db, password) and check_email == "YES":
      return user
    elif check_password_hash(passwrod_db, password) and check_email == "NO":
      return "EMAIL_NOT_VALID"
    else:
      return None
      
# link the user for longing
def get_user_by_id(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts_admin WHERE id = :id"), dict(id=id))
    row = result.fetchone()  
    if row != None:
      logged_user = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
      #Arquive the user in session
      session["id"] = logged_user.id
      session["email"] = logged_user.email
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