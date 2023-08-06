from sqlalchemy import create_engine, text
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Class for itentify user
from User import User

my_secret = os.environ['DB_CARFLEET']

engine =create_engine(my_secret,connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}})

# Car database
def car_inf_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM car_inf"))
    car_inf_dicts = []
    result_all = result.all()
    number_register = len(result_all)
    for row in range(number_register):
      car_inf_dicts.append(result_all[row]._mapping)
    return car_inf_dicts

# User Datase
def users_dicts(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts"))
    users_dicts = []
    result_all = result.all()
    number_register = len(result_all)
    for row in range(number_register):
       users_dicts.append(result_all[row]._mapping)
    return users_dicts

# Selected the car by ID
def cars_inf_db(id):
 with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM car_inf"))
    result_all = result.all()
    id_int = int(id)
    id_int = id_int -1
    car_inf_dicts = result_all[int(id_int)]
    return car_inf_dicts

# Car Registration
def add_car_reg_db(data):
  with engine.connect() as conn:
   query = text("INSERT INTO applications (maker, made, year, comments) VALUES (:maker, :made, :year, :comments)")
   conn.execute(query, data)

# Check the Login
def login_check1(username, password):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts WHERE username = :username"), dict(username=username))
    user = result.fetchone()
    user = User(user[0], user[1], user[2], user[3])
    passwrod_db = user.password
    print('Password:', password)
    if check_password_hash(passwrod_db, password):
      print(user)
      return user
    else:
        return None

# link the user for longing
def get_user_by_id(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts WHERE id = :id"), dict(id=id))
    row = result.fetchone()  
    print(row)
    if row != None:
      logged_user = User(row[0], row[1], row[2], row[3])
      return logged_user
    else:
      return None

# User Register in the Database Accounts.
def signupuser(data):
  username = data['username']
  password = data['password']
  password = generate_password_hash(password)
  email = data['email']
  user_add = {"username": username, "password": password, "email": email}
  print(type(user_add))
  print(user_add)
  with engine.connect() as conn:
    query = text("INSERT INTO accounts (username, password, email) VALUES (:username, :password, :email)")
    conn.execute(query, user_add)
  return