from sqlalchemy import create_engine, text
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Class for itentify user
from User import User

my_secret = os.environ['DB_CARFLEET']

engine =create_engine(my_secret,connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}})


# Check the Login
def login_check1(email, password):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts WHERE email = :email"), dict(email=email))
    user = result.fetchone()
    if not user:
      return None
    user = User(user[0], user[1], user[2])
    passwrod_db = user.password
    if check_password_hash(passwrod_db, password):
      return user
    else:
        return None

# link the user for longing
def get_user_by_id(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts WHERE id = :id"), dict(id=id))
    row = result.fetchone()  
    if row != None:
      logged_user = User(row[0], row[1], row[2])
      return logged_user
    else:
      return None

# User Register in the Database Accounts.
def signupuser(data):
  email = data['email']
  password = data['password']
  password = generate_password_hash(password)
  user_add = {"email": email, "password": password}

  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts WHERE email = :email"), dict(email=email))

  if len(result.all())!=0:
    return "USER_EXISTE"
  else:  
    with engine.connect() as conn:
      query = text("INSERT INTO accounts (email, password) VALUES (:email, :password)")
      conn.execute(query, user_add)
    return "SIGNEDUP"
