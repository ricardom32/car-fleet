from database import car_inf_db, cars_inf_db, add_car_reg_db, login_check1, signupuser, get_user_by_id
#from flask import url_for

# Config used to upload the file
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/dashboard/<id>')
def dashboard(id):
  dashboard = cars_inf_db(id)
  return render_template('dashboard.html',dashboard=dashboard)

@app.route("/car_inf/<id>/apply", methods=["post"])
def apply_to_car(id):
  data = request.form
  add_car_reg_db(data)
  return render_template('car_reg_submit.html',car_reg=data)


@app.route("/api/car_inf/<id>")
def list_car_inf(id):
  car_inf=cars_inf_db(id)
  return jsonify(car_inf)