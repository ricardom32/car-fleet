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