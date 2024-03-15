from sqlalchemy import create_engine, text
import os

my_secret = os.environ['DB_CARFLEET']
#my_secret = os.environ['DB_CARS-FLEET_AIVEN']
engine =create_engine(my_secret,connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}}, isolation_level="AUTOCOMMIT")

# New customer account. 
def car_register(data):
  with engine.connect() as conn:
   query = text("INSERT INTO car_register (user_email, user_id, nick_name, make, model, year, color, vin, plate) VALUES (:user_email, :user_id, :nick_name, :make, :model, :year, :color, :vin, :plate)")
   conn.execute(query, data)
   
  with engine.connect() as conn:
    result = conn.execute(text("SELECT last_insert_id() from car_register"))
  
  last_id = result.fetchone() 
  last_id=str(last_id)
  last_id=last_id.replace('(','').replace(')','').replace(',','')
  print(type(last_id))
  last_id={
    "id": last_id,
    "user_id": last_id
  }
  print(last_id)
  with engine.connect() as conn:
   query = text("UPDATE car_register SET user_id = :user_id WHERE id =:id")
   conn.execute(query,last_id)

# New customer account.
def db_car_search(data):
  search_type = data['search_type']
  search_field = data['search']
  user_email = data['user_email']
  if search_type == "nick_name":
    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM car_register WHERE nick_name = :search_field and user_email = :user_email"), dict(search_field=search_field, user_email=user_email))
  elif search_type == "make":
    with engine.connect() as conn: 
      result = conn.execute(text("SELECT * FROM car_register WHERE make = :search_field and user_email = :user_email"), dict(search_field=search_field, user_email=user_email))
  elif search_type == "model":
    with engine.connect() as conn: 
      result = conn.execute(text("SELECT * FROM car_register WHERE model = :search_field and user_email = :user_email"), dict(search_field=search_field, user_email=user_email))
  elif search_type == "year":
    with engine.connect() as conn: 
      result = conn.execute(text("SELECT * FROM car_register WHERE year = :search_field and user_email = :user_email"), dict(search_field=search_field, user_email=user_email))
  elif search_type == "vin":
    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM car_register WHERE vin = :search_field and user_email = :user_email"), dict(search_field=search_field, user_email=user_email))
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
    conn.execute(text("TRUNCATE TABLE search_car"))
  
  #Update the Search account table with new value searched. 
  with engine.connect() as conn:
    query = text("INSERT INTO search_car (user_email, user_id, nick_name, make, model, year, color, vin, plate) VALUES (:user_email, :user_id, :nick_name, :make, :model, :year, :color, :vin, :plate)")
    conn.execute(query, search_account_dict)
    return search_account_dict

def detail_car(id):
  id=int(id)+1
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM search_car WHERE id = :id"), dict(id=id))
    search_car_dict = []
    result_all = result.fetchone() 
    search_car_dict.append(result_all._mapping)
    search_car_dict=search_car_dict[0]
  
  #Delete all the data from Search Account table
  with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE search_car"))
  
  with engine.connect() as conn:
    query = text("INSERT INTO search_car (user_email, user_id, nick_name, make, model, year, color, vin, plate) VALUES (:user_email, :user_id, :nick_name, :make, :model, :year, :color, :vin, :plate)")
    conn.execute(query, search_car_dict)
    return search_car_dict

def edit_car():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM search_car"))
    car_edit_dicts = []
    result_all = result.fetchone()
    car_edit_dicts.append(result_all._mapping)
    car_edit_dicts=car_edit_dicts[0]
    return car_edit_dicts

# Updated Customer account. 
def db_car_updated(data):
  with engine.connect() as conn:
    query = text("UPDATE car_register SET user_email = :user_email, user_id = :user_id, nick_name = :nick_name,  make = :make, model = :model, year = :year, color = :color, vin = :vin, plate =:plate WHERE user_id = :user_id and user_email = :user_email") 
    conn.execute(query,data)

