from flask import Blueprint
from flask import render_template
from flask_login import login_required

#Defining a Blueprint
app_pricetable = Blueprint('app_pricetable',__name__)

# This call the price table
@app_pricetable.route('/forms/pricetable')
@login_required
def price_table():
  return render_template('/form_pricetable.html') 