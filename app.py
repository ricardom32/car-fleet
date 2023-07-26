from flask import Flask, render_template, jsonify, request
from database import car_inf_db, cars_inf_db, add_car_reg_db, login_check

app = Flask(__name__)

@app.route("/")
def Car_easy_fleet():
  car_inf = car_inf_db()
  return render_template('home.html', car_inf=car_inf, company_name='Car Fleet')

@app.route("/api/car_inf/<id>")
def list_car_inf(id):
  car_inf=cars_inf_db(id)
  return jsonify(car_inf)

@app.route('/dashboard/<id>')
def dashboard(id):
  dashboard = cars_inf_db(id)
  return render_template('dashboard.html',dashboard=dashboard)

@app.route("/car_inf/<id>/apply", methods=["post"])
def apply_to_car(id):
  data = request.form
  add_car_reg_db(data)
  return render_template('car_reg_submit.html',car_reg=data)

@app.route('/login.html')
def login():
  return render_template('/login.html')

@app.route('/login/apply', methods=['GET', 'POST'])
def login_a():
    # Output a message if something goes wrong...
    msg = 'Output a message if something goes wrong...'
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
    return jsonify(password)

@app.route('/signup.html')
def signup():
  return render_template('/signup.html')

@app.route('/signup/apply')
def signupaccount():
  return render_template('/useraccount.html')

@app.route('/index.html')
def meubar():
  return render_template('/index.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
