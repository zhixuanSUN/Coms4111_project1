
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response,url_for,flash,jsonify
import json

#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
#app = Flask(__name__, template_folder=tmpl_dir)
app = Flask(__name__)

DB_USER = "jz3518"
DB_PASSWORD = "3214"
DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"
#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)
@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request
  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('pwd')
    if username == "1" and password == "1":
        return render_template("index.html", msg="login successfully")
    else:
        return render_template("login.html", msg="Fail. Please try again")

@app.route('/quality')
def quality():
    data = g.conn.execute("SELECT * FROM drinking_water_quality")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("quality.html", tophat = tophat, name = "drinking_water_quality")

@app.route('/Back')
def Back():
    return render_template("index.html")

@app.route('/Profile')
def profile():
    data = g.conn.execute("SELECT * FROM users where uid = 1 ")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("profile.html", tophat=tophat, name="users")

@app.route('/Donation')
def donation():
    return render_template("donation.html")

@app.route('/Events')
def events():
    data = g.conn.execute("SELECT * FROM events ")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("events.html", tophat=tophat, name="Events")

@app.route('/takeevent', methods=['GET','POST'])
def takeevent():
    if request.method == 'POST':
        uid = request.form.get('uid')
        eventid = request.form.get('eventid')
        intuid = int(uid)
        inteventid = int(eventid)
        # if not uid or not eventid:
        #     return render_template("takeevent.html")
        try:
            cursor = g.conn.cursor()
            sql = "INSERT INTO take VALUES (1.2)"
            #sql ="INSERT INTO take VALUES (%d,%d)" %(intuid, inteventid)
            cursor.execute(sql)
            g.conn.commit()
            cursor.close()
            return "success"
        except:
            return render_template("takeevent.html")

    if request.method == 'GET':
        return render_template("takeevent.html")

@app.route('/add')
def add():
    sql = "INSERT INTO take VALUES (1,2)"
    g.conn.execute(sql)
    data = g.conn.execute("SELECT * FROM take ")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("add.html", tophat=tophat, name="add")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8111)

