from sqlalchemy import create_engine, text
import os

my_secret = os.environ['DB_CARFLEET']

engine =create_engine(my_secret,connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}})


def detail_account(id):
  id=int(id)+1
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM search_account1 WHERE id = :id"), dict(id=id))
    search_account_dict = []
    result_all = result.fetchone() 
    search_account_dict.append(result_all._mapping)
    search_account_dict=search_account_dict[0]

  #Delete all the data from Search Account table
  with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE search_account1"))
  
  with engine.connect() as conn:
    query = text("INSERT INTO search_account1 (user_email, user_id, first_name, last_name, date_birth, email, mobile, gender, occupation, dl_number, dl_country, dl_expired, address, complements, city, state,coutry, zipcode, photo) VALUES (:user_email, :user_id, :first_name, :last_name, :date_birth, :email, :mobile, :gender, :occupation, :dl_number, :dl_country, :dl_expired, :address, :complements, :city, :state, :coutry, :zipcode, :photo)")
    conn.execute(query, search_account_dict)
    return search_account_dict

def edit_user():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM search_account1"))
    user_edit_dicts = []
    result_all = result.fetchone()
    user_edit_dicts.append(result_all._mapping)
    user_edit_dicts=user_edit_dicts[0]
    return user_edit_dicts

# Updated Customer account. 
def db_customer_updated(data):
  user_id = data['user_id']
  first_name=data["first_name"]
  user_email = data['user_email']

  with engine.connect() as conn:
    query = text("UPDATE customer_account_1 SET user_email = :user_email, user_id = :user_id, first_name = :first_name,  last_name = :last_name, date_birth = :date_birth, email = :email, mobile = :mobile, gender = :gender, occupation =:occupation, dl_number = :dl_number, dl_country =:dl_country, dl_expired =:dl_expired, address =:address, complements = :complements, city = :city, state = :state, coutry = :coutry, zipcode = :zipcode, photo = :photo WHERE user_id = :user_id and user_email = :user_email") 
    conn.execute(query,data)
