from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
  def __init__(self, id,  email_admin, password_admin, email, password,first_name, last_name, date_birth):
    self.id = id
    self.email_admin = email
    self.password_admin = password
    self.email = email
    self.password = password
    self.first_name = first_name
    self.last_name = last_name
    self.date_birth = date_birth


  @classmethod
  def check_password(self, hashed_password, password):
    return check_password_hash(hashed_password, password)
