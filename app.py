
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response,url_for,flash,jsonify
import json

#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
#app = Flask(__name__, template_folder=tmpl_dir)
# tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
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
    if username == "1" and password == "AA":
        return render_template("index.html", msg="login successfully")
    else:
        return render_template("login.html", msg="Fail. Please try again(username is 1 and password is AA)")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    if request.method == 'POST':
        uid = request.form.get('uid')
        name = request.form.get('name')
        password = request.form.get('password')
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


@app.route('/quality')
def quality():
    data = g.conn.execute("SELECT * FROM drinking_water_quality")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("quality.html", tophat = tophat, name = "Drinking_Water_Quality")


@app.route('/Search_quality',methods=['POST'])
def search_quality():
    try:
        sample_number = request.values.get('sample_number')
        if not sample_number:
            return render_template("Error.html")
        else:
            data = g.conn.execute("SELECT * FROM drinking_water_quality where (sample_number ='%s')" %(sample_number))
        column_names = data.keys()
        tophat = []
        tophat.append(column_names)
        for row in data:
            tophat.append(row)
        return render_template("quality.html", tophat=tophat, name="Quality")
    except:
        return render_template("Error.html")


@app.route('/List')
def list():
    data = g.conn.execute("SELECT * FROM list")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("list.html", tophat=tophat, name="Users_Data_List")


@app.route('/Search_list',methods=['POST'])
def lists():
    try:

        uid = request.values.get('uid')
        if not uid:
            return render_template("Error.html")
        else:
            data = g.conn.execute("SELECT * FROM list where (uid ='%s')" %(uid))
        column_names = data.keys()
        tophat = []
        tophat.append(column_names)
        for row in data:
            tophat.append(row)
        return render_template("list.html", tophat=tophat, name="Selected_User_List")
    except:
        return render_template("Error.html")


@app.route('/add', methods=['POST'])
def add():
    try:
        list_id = request.form['list_id']
        time = request.form['time']
        detail = request.form['detail']
        uid = request.form['uid']
        if not list_id or not time or not detail or not uid:
            return render_template("Error.html")
        else:
            g.conn.execute('INSERT INTO list(list_id,time,detail,uid) VALUES (%s,%s,%s,%s);',(list_id,time,detail,uid))
        return render_template('index.html')
    except:
        return render_template('Error.html')


@app.route('/Issues')
def issues():
    data = g.conn.execute("SELECT * FROM issues")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("issues.html", tophat=tophat, name="issues")


@app.route('/add1', methods=['POST'])
def add1():
    try:
        issue_id = request.form['issue_id']
        time = request.form['time']
        location = request.form['location']
        description = request.form['description']
        if not issue_id or not time or not location or not description:
            return render_template("Error.html")
        else:
            g.conn.execute('INSERT INTO issues(issue_id,time,location,description) VALUES (%s,%s,%s,%s);',(issue_id,time,location,description))
        return render_template('index.html')
    except:
        return render_template("Error.html")


@app.route('/comments')
def comments():
    data = g.conn.execute("SELECT * FROM comments")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("comments.html", tophat=tophat, name="Comments")


@app.route('/add2', methods=['POST'])
def add2():
    try:
        comment_id = request.form['comment_id']
        content = request.form['content']
        time = request.form['time']
        issue_id = request.form['issue_id']
        if not comment_id or not content or not time or not issue_id:
            return render_template('Error.html')
        else:
            g.conn.execute('INSERT INTO comments(comment_id,content,time,issue_id) VALUES (%s,%s,%s,%s);',(comment_id,content,time,issue_id))
        return render_template('index.html')
    except:
        return render_template('Error.html')


@app.route('/Events')
def event():
    data = g.conn.execute("SELECT * FROM events")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("events.html", tophat=tophat, name="Events")


@app.route('/takeevent')
def take():
    data = g.conn.execute("SELECT * FROM take")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("takeevent.html", tophat=tophat, name="Participation")


@app.route('/add3', methods=['POST'])
def add3():
    try:
        take_id = request.form['take_id']
        uid = request.form['uid']
        event_id = request.form['event_id']
        if not take_id or not uid or not event_id:
            return render_template('Error.html')
        else:
            g.conn.execute('INSERT INTO take(take_id,uid,event_id) VALUES (%s,%s);',(take_id,uid,event_id))
        return render_template('index.html')
    except:
        return render_template('Error.html')


@app.route('/donation')
def donation():
    data = g.conn.execute("SELECT * FROM donation")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("donation.html", tophat=tophat, name="donation")


@app.route('/add4', methods=['POST'])
def add4():
    try:
        donation_id = request.form['donation_id']
        amount = request.form['amount']
        time = request.form['time']
        if not donation_id or not amount or not time:
            return render_template("Error.html")
        else:
            #cmd = 'INSERT INTO list(list_id,time,detail,uid) VALUES (%s,%s,%s,%s);'%(list_id,time,detail,uid)
            g.conn.execute('INSERT INTO donation(donation_id, amount, time) VALUES (%s,%s,%s);',(donation_id, amount, time))
        return render_template('index.html')
    except:
        return render_template('Error.html')


@app.route('/Back')
def Back():
    return render_template("index.html")


if __name__ == '__main__':
    import click


    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
    run()

