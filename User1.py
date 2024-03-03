from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
  def __init__(self, id, email_admin, email, password,first_name, last_name, reservation_main, reservation_reg, reservation_detail, customer_main, customer_reg, customer_detail, maintenance_main, maintenance_reg, maintenance_detail, car_main, car_reg, car_detail, team_main, team_reg, team_detail, employee_main, employee_reg, employee_detail, expense_main, expense_reg, expense_detail, view_plan):
    
    self.id = id
    self.email_admin = email
    self.email = email
    self.password = password
    self.first_name = first_name
    self.last_name = last_name
    self.reservation_main = reservation_main
    self.reservation_reg =reservation_reg
    self.reservation_detail = reservation_detail
    self.customer_main = customer_main
    self.customer_reg = customer_reg
    self.customer_detail = customer_detail
    self.maintenance_main = maintenance_main
    self.maintenance_reg = maintenance_reg
    self.maintenance_detail = maintenance_detail
    self.car_main = car_main
    self.car_reg = car_reg
    self.car_detail = car_detail
    self.team_main = team_main
    self.team_reg = team_reg
    self.team_detail = team_detail
    self.employee_main = employee_main
    self.employee_reg = employee_reg
    self.employee_detail = employee_detail
    self.view_plan = view_plan
  
  @classmethod
  def check_password(self, hashed_password, password):
    return check_password_hash(hashed_password, password)
