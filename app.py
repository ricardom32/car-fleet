from flask import Flask, render_template, jsonify
from database import car_inf_db, cars_inf_db

app = Flask(__name__)

@app.route("/")
def Car_easy_fleet():
  car_inf = car_inf_db()
  return render_template('home.html', car_inf=car_inf, company_name='Car Fleet')

@app.route("/api/car_inf")
def list_car_inf():
  car_inf=car_inf_db()
  return jsonify(car_inf)

@app.route('/dashboard/<id>')
def dashboard(id):
  dashboard = cars_inf_db(id)
  return render_template('dashboard.html',dashboard=dashboard)
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
