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

#data = {
#  "maker": "Ford",
#  "made": "Mustang",
#  "year": 1964,
#  "comments": "Teste of database",
#}
#add_car_reg_db(data)

# Check the Login
def login_check1(username, password):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts WHERE username = :username"), dict(username=username))
    user = result.fetchone()
    if not user:
      return None
    user = User(user[0], user[1], user[2], user[3])
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
  with engine.connect() as conn:
    query = text("INSERT INTO accounts (username, password, email) VALUES (:username, :password, :email)")
    conn.execute(query, user_add)
  return

# New customer account. 
def db_new_account(data):
  with engine.connect() as conn:
   query = text("INSERT INTO customer_account (first_name, last_name, date_birth, email, mobile, gender, occupation, dl_number, dl_country, dl_expired, address, complements, city, state,coutry, zipcode) VALUES (:first_name, :last_name, :date_birth, :email, :mobile, :gender, :occupation, :dl_number, :dl_country, :dl_expired, :address, :complements, :city, :state, :coutry, :zipcode)")
   conn.execute(query, data)

# New customer account.
def db_customer_search(data):
  search_type = data['search_type']
  search_field = data['search']
  if search_type == "first_name":
    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM customer_account WHERE first_name = :search_field"), dict(search_field=search_field))
  elif search_type == "last_name":
    with engine.connect() as conn: result = conn.execute(text("SELECT * FROM customer_account WHERE last_name = :search_field"), dict(search_field=search_field))
  elif search_type == "email":
    with engine.connect() as conn: result = conn.execute(text("SELECT * FROM customer_account WHERE email = :search_field"), dict(search_field=search_field))
  elif search_type == "mobile":
    with engine.connect() as conn: result = conn.execute(text("SELECT * FROM customer_account WHERE mobile = :search_field"), dict(search_field=search_field))
  elif search_type == "dl_number":
    with engine.connect() as conn: result = conn.execute(text("SELECT * FROM customer_account WHERE dl_number = :search_field"), dict(search_field=search_field))
  else: return None
  
  search_account_dict = []
  result_all = result.all()
  number_register = len(result_all)
  if number_register == 0: return None
  for row in range(number_register):
    search_account_dict.append(result_all[row]._mapping)

 #Delete all the data from Search Account table
  with engine.connect() as conn:
    #conn.execute(text("DELETE FROM search_account"))
    conn.execute(text("TRUNCATE TABLE search_account"))
  
  #Update the Search account table with new value searched. 
  with engine.connect() as conn:
    query = text("INSERT INTO search_account (user_id, first_name, last_name, date_birth, email, mobile, gender, occupation, dl_number, dl_country, dl_expired, address, complements, city, state,coutry, zipcode) VALUES (:user_id, :first_name, :last_name, :date_birth, :email, :mobile, :gender, :occupation, :dl_number, :dl_country, :dl_expired, :address, :complements, :city, :state, :coutry, :zipcode)")
    conn.execute(query, search_account_dict)
    return search_account_dict

def detail_account(id):
  id=int(id)+1
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM search_account WHERE id = :id"), dict(id=id))
    search_account_dict = []
    result_all = result.fetchone() 
    search_account_dict.append(result_all._mapping)
    search_account_dict=search_account_dict[0]
  
  #Delete all the data from Search Account table
  with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE search_account"))
  
  with engine.connect() as conn:
    query = text("INSERT INTO search_account (user_id, first_name, last_name, date_birth, email, mobile, gender, occupation, dl_number, dl_country, dl_expired, address, complements, city, state,coutry, zipcode) VALUES (:user_id, :first_name, :last_name, :date_birth, :email, :mobile, :gender, :occupation, :dl_number, :dl_country, :dl_expired, :address, :complements, :city, :state, :coutry, :zipcode)")
    conn.execute(query, search_account_dict)
    return search_account_dict

def edit_user():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM search_account"))
    user_edit_dicts = []
    result_all = result.fetchone()
    user_edit_dicts.append(result_all._mapping)
    user_edit_dicts=user_edit_dicts[0]
    return user_edit_dicts

# Updated Customer account. 
def db_customer_updated(data):
  user_id = data['user_id']
  first_name=data["first_name"]
  #user_id = tuple(user_id)
  print(type(user_id))
  print(type(data))
  print(data)
  print(user_id)
  
#  with engine.connect() as conn:
#    query = text("DELETE FROM customer_account WHERE user_id = :user_id") 
#    conn.execute(query,data)

  with engine.connect() as conn:
    #query = text("DELETE FROM customer_account WHERE user_id = :user_id") 
    #query = text("UPDATE customer_account SET first_name = :first_name WHERE user_id = :user_id") 
    #conn.execute(query,data)
    query = text("UPDATE customer_account SET user_id = :user_id, first_name = :first_name,  last_name = :last_name, date_birth = :date_birth, email = :email, mobile = :mobile, gender = :gender, occupation =:occupation, dl_number = :dl_number, dl_country =:dl_country, dl_expired =:dl_expired, address =:address, complements = :complements, city = :city, state = :state, coutry = :coutry, zipcode = :zipcode WHERE user_id = :user_id") 
    conn.execute(query,data)
  
 # with engine.connect() as conn:
  #  query = text("INSERT INTO customer_account (user_id, first_name, last_name, date_birth, email, mobile, gender, occupation, dl_number, dl_country, dl_expired, address, complements, city, state,coutry, zipcode) VALUES (:user_id, :first_name, :last_name, :date_birth, :email, :mobile, :gender, :occupation, :dl_number, :dl_country, :dl_expired, :address, :complements, :city, :state, :coutry, :zipcode) ")
  #  conn.execute(query,data)
  

  #with engine.connect() as conn:
  #  result = conn.execute(text("SELECT * FROM search_account"))
  #  users_dicts = []
  #  result_all = result.all()
  #  number_register = len(result_all)
  #  for row in range(number_register):
  #     users_dicts.append(result_all[row]._mapping)
 
  #with engine.connect() as conn:
  #  query = text("UPDATE customer_account SET first_name = 'Teste' WHERE user_id = 1") 
  #  conn.execute(query)
    #query = text("INSERT INTO search_account (user_id, first_name, last_name, date_birth, email, mobile, gender, occupation, dl_number, dl_country, dl_expired, address, complements, city, state,coutry, zipcode) VALUES (:user_id, :first_name, :last_name, :date_birth, :email, :mobile, :gender, :occupation, :dl_number, :dl_country, :dl_expired, :address, :complements, :city, :state, :coutry, :zipcode) ON DUPLICATE KEY UPDATE last_name = 'Garcia2' ")
    #conn.execute(query)

  #with engine.connect() as conn:
  #  result = conn.execute(text("SELECT * FROM search_account"))

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
#db_new_account(data)