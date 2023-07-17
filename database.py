from sqlalchemy import create_engine, text
import os
my_secret = os.environ['DB_CARFLEET']

engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  })

with engine.connect() as conn:
  result = conn.execute(text("select * from jobs"))
  print(result.all())