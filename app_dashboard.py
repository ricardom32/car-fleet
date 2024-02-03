# Car_app Routing
from flask import Blueprint
from flask import render_template
from flask_login import login_required

#Defining a Blueprint
app_dashboard = Blueprint('app_dashboard',__name__)

# Car Information
@app_dashboard.route('/forms/dashboard')
@login_required
def car_registration():
  return render_template('/form_dashboard.html')
