from sqlalchemy import create_engine, text
import os

my_secret = os.environ['DB_CARFLEET']

engine = create_engine(my_secret,connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}})

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
    result = conn.execute(text("SELECT * FROM car_inf WHERE id")
    result_all = result.all()
    car_inf_dicts = result_all[id]._mapping
    return car_inf_dicts