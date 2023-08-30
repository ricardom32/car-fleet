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
"""
data1 = {
  "first_name": "Ford",
  "last_name": "Mustang",
  "date_birth": "2023-08-20",
  "email": "ricardom32@hotmail.com",
  "mobile": 1234567,
  "gender": "Femele",
  "occupation": "Engineer",
  "dl_number": "12345655",
  "dl_country": "United States",
  "dl_expiry_date": "2023-08-20",
  "address": "1358 Las Juntas Way Apt G",
  "complements": "G",
  "city": "Walnut Creek",
  "state": "California",
  "coutry": "Brazil",
  "zipcode": "94597",
}
"""