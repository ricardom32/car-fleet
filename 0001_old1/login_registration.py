import flask, request, template, redirect
import os
import sqlite3

currentlocation = os.path.dirname(cs.path.abspath(__file__))

myapp = Flask(__name__)

@myapp.route("/")
def home():
  return render_template("homepage.html")

@myapp.route("/", methods = ["Post"])
def checklogin():
  UN = request.form['username']
  PW = request.form['password']

sqlconnection = sqlite3.Connection(currentlocation + "\Login.dp")
cursor = sqlconnection.cursor()
query1 = "SELECT username, Password from Users WHERE Username = '{un}' and Password = '{pw}'",format(un = UN, pw = PW)

rows = curson.execute(query1)
rows = rows.fetchall()
if len(rows)==1:
  return render_template("Loggedin.html")
else:
  return reducrect("/register")

@myapp.route("/register", methods["GET", "POST"])
def registerpage():
  if request.method == "POST":
    dUN = request.form['Dusername']
    dPW = request.form['Dpassword']
    Uemail = request.form['Emailuser']
    sqlconnection = sqlite3.Connection(currentlocation + "\Login.db")
    cursor = sqlconnection.cursor()
    query1 = "INSERT INTO User VALUES('{u}','{p}','{e}')".format(u =dUN, p = dPw, e = Uemail)
    cursor.excute(query1)
    sqlconnection.commit()
    return redirect("/")
return render_template("Regirster.html")

if __name__ == "__main__":
  myapp.run()
