from sqlalchemy import create_engine, text
import os


my_secret = os.environ['DB_CARFLEET']

engine =create_engine(my_secret,connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}})

def car_inf_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM car_inf"))
    car_inf_dicts = []
    result_all = result.all()
    number_register = len(result_all)
    for row in range(number_register):
      car_inf_dicts.append(result_all[row]._mapping)
    return car_inf_dicts

def cars_inf_db(id):
 with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM car_inf"))
    result_all = result.all()
    id_int = int(id)
    id_int = id_int -1
    car_inf_dicts = result_all[int(id_int)]
    return car_inf_dicts

def add_car_reg_db(data):
  with engine.connect() as conn:
   query = text("INSERT INTO applications (maker, made, year, comments) VALUES (:maker, :made, :year, :comments)")
   conn.execute(query, data)

def login_check1(username, password):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM accounts WHERE username = :username"), dict(username=username))
    for row in result.mappings():
      if password == row['password']:
        return 'uerloged'
      else:
        return 'userfailed'

data = {
  "username": 'tes1',
  "password": 'newpass',
  "email": 'maga@hotmail.com'
 }

def signupuser(data):
  with engine.connect() as conn:
    query = text("INSERT INTO accounts (username, password, email) VALUES (:username, :password, :email)")
    conn.execute(query, data)
  return

#signupuser(data)


with engine.connect() as conn:
  result = conn.execute(text("SELECT * FROM accounts"))
  result_all = result.all()
  id_int = int(1)
  id_int = id_int -1
  car_inf_dicts = result_all[int(id_int)]
  print(result_all)



    

