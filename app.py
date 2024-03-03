from flask import Flask, render_template, session
from db_loging import get_user_by_id
#import secrets

from flask_mail import Mail

#Blueprint library
from app_car import app_car
from app_customer import app_customer
from app_maintenance import app_maintenance
from app_reservation import app_reservation
from app_employee import app_employee
from app_expense import app_expense
from app_dashboard import app_dashboard
from app_profile import app_profile
from app_pricetable import app_pricetable
from app_team import app_team
from app_loging import app_loging

# project the access the database with Token
from flask_wtf.csrf import CSRFProtect

# login
from flask_login import LoginManager, logout_user, login_required

# import modules Flask and Bluprints
app = Flask(__name__)
app.register_blueprint(app_car)
app.register_blueprint(app_customer)
app.register_blueprint(app_maintenance)
app.register_blueprint(app_reservation)
app.register_blueprint(app_employee)
app.register_blueprint(app_expense)
app.register_blueprint(app_dashboard)
app.register_blueprint(app_profile)
app.register_blueprint(app_pricetable)
app.register_blueprint(app_team)
app.register_blueprint(app_loging)

#Google SMTP server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'carsfleetus@gmail.com'
app.config['MAIL_PASSWORD'] = 'abla qqag tyku znxr'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
# Random OPT code
#otp = randint(100000, 999999)

# CSRFProtect
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)
app.config['SECRET_KEY'] = 'thisisasecretkeyforcarfleet'

@app.route("/")
def Car_easy_fleet():
  #print("Ricardo_teste1",load_user.email)
  return render_template('/home.html', company_name='Cars-Fleet')

#identify the user
@login_manager_app.user_loader
def load_user(id):
  return get_user_by_id(id)

#Open the page with logged user
@app.route('/userlogged')
@login_required
def user_loged():
  return render_template('/form_dashboard.html')

@app.route('/logout')
def logout():
  # remove the username from the session if it is there
  session["id"] = None
  session["email"] = None
  logout_user()
  return render_template('/home.html')

if __name__ == "__main__":
  csrf.init_app(app)
  app.run(host='0.0.0.0', debug=True)
