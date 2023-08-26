from sqlalchemy import create_engine, text
import os

my_secret = os.environ['DB_CARFLEET']

engine =create_engine(my_secret,connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}})

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
    print("teste_firtname")
    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM customer_account WHERE first_name = :search_field"), dict(search_field=search_field))
  elif search_type == "last_name":
    with engine.connect() as conn: 
      result = conn.execute(text("SELECT * FROM customer_account WHERE last_name = :search_field"), dict(search_field=search_field))
  elif search_type == "email":
    with engine.connect() as conn: 
      result = conn.execute(text("SELECT * FROM customer_account WHERE email = :search_field"), dict(search_field=search_field))
  elif search_type == "mobile":
    with engine.connect() as conn: 
      result = conn.execute(text("SELECT * FROM customer_account WHERE mobile = :search_field"), dict(search_field=search_field))
  elif search_type == "dl_number":
    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM customer_account WHERE dl_number = :search_field"), dict(search_field=search_field))
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


  with engine.connect() as conn:
    query = text("UPDATE customer_account SET user_id = :user_id, first_name = :first_name,  last_name = :last_name, date_birth = :date_birth, email = :email, mobile = :mobile, gender = :gender, occupation =:occupation, dl_number = :dl_number, dl_country =:dl_country, dl_expired =:dl_expired, address =:address, complements = :complements, city = :city, state = :state, coutry = :coutry, zipcode = :zipcode WHERE user_id = :user_id") 
    conn.execute(query,data)
  