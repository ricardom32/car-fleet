from sqlalchemy import create_engine, text
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import ImmutableMultiDict

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
#def login_check1(username, password):
#  with engine.connect() as conn:
#    result = conn.execute(text("SELECT * FROM accounts WHERE username = :username"), dict(username=username))
#    for row in result.mappings():
#      if password == row['password']:
#        return 'user_loggedin'
#      else:
#        return 'Failed_loggedin'

#username = 'ricardom32'
#password = 'Rgtmri930#1'

# Check the Login
def login_check1(username, password):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts WHERE username = :username"), dict(username=username))
    user = result.fetchone()
    user = User(user[0], user[1], user[2], user[3])
    passwrod_db = user.password
    print('Password:', password)
    #for row in result:
    #if password == passwrod_db:
    if check_password_hash(passwrod_db, password):
      print(user)
      return user
    else:
        return None

#print(login_check1(username, password))

# link the user for longing
def get_user_by_id(id):
  with engine.connect() as conn:
    #result = conn.execute(text("SELECT * FROM accounts WHERE id = {}".format(id)))
    result = conn.execute(text("SELECT * FROM accounts WHERE id = :id"), dict(id=id))
    row = result.fetchone()  
    #result = User(2, 'ricardom32', 'Rgtmri930#1', 'ricardom32@hotmail.com')
    #row = result.fetchone()  
    print(row)
    if row != None:
      logged_user = User(row[0], row[1], row[2], row[3])
      return logged_user
    else:
      return None

#print(get_user_by_id(2))

# User Register in the Database Accounts.
def signupuser(data):
  #data1 = data.to_dic(flat=false)
  #data.to_dict(flat=True)
  #print(data)
  username = data['username']
  password = data['password']
  password = generate_password_hash(password)
  email = data['email']
  user_add = {"username": username, "password": password, "email": email}
  
  #password = generate_password_hash(password)
  #print(password)
  #data.set(data['password'],password)
  #print.lists(data)
  #data['password'] = password
  
  #print(data.value['password'])
  # data.password = generate_password_hash(data.password)
  # print(data.password)
  print(type(user_add))
  print(user_add)
  with engine.connect() as conn:
    query = text("INSERT INTO accounts (username, password, email) VALUES (:username, :password, :email)")
    conn.execute(query, user_add)
  return



#username = 'ricardom32'
#password = 'Rgtmri930#1'

#login_check1(username,password)

#def logged_user(username, password):
#  with engine.connect() as conn:
#    result = conn.execute(text("SELECT * FROM accounts WHERE username = :username"), dict(username=username))
#    result_cursor = conn.
#    row = cursor.fetchone()
    #print(row)
#    return row


#print(logged_user(username, password))

#data = {
#  "username": 'tes1',
#  "password": 'newpass',
#  "email": 'maga@hotmail.com'
# }

#signupuser(data)

with engine.connect() as conn:
  result = conn.execute(text("SELECT * FROM accounts"))
  result_all = result.all()
  id_int = int(1)
  id_int = id_int -1
  car_inf_dicts = result_all[int(id_int)]
  print(result_all)
