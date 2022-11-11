#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)



# XXX: The Database URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/<DB_NAME>
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# For your convenience, we already set it to the class database

# Use the DB credentials you received by e-mail
DB_USER = "hl3434"
DB_PASSWORD = "7774"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


# Here we create a test table and insert some values in it
# engine.execute("""DROP TABLE IF EXISTS test;""")
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")



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


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
#   cursor = g.conn.execute("SELECT name FROM test")
#   names = []
#   for result in cursor:
#     names.append(result['name'])  # can also be accessed using result[0]
#   cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
#   context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
#   return render_template("index.html", **context)
  return render_template("base.html")

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
# @app.route('/another')
# def another():
#   return render_template("anotherfile.html")


# # Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add():
#   name = request.form['name']
#   print(name)
#   cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)';
#   g.conn.execute(text(cmd), name1 = name, name2 = name);
#   return redirect('/')


# @app.route('/login')
# def login():
#     abort(401)
#     this_is_never_executed()

@app.route('/Supplier')
def Supplier():
    data = g.conn.execute("SELECT * FROM Supplier Order by Supplier_id")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Supplier_information.html",tophat = tophat,name="Supplier")

@app.route('/Search_Supplier', methods = ['POST'])
def Search_Supplier():
    option = request.values.get("option")
    id = request.values.get('supplier_id')
    if not id or not option:
        return render_template("ERROR.html")
    if option == 'Supplier id' and not id.isdigit():
        return render_template("ERROR.html")
    
    if option == "Supplier id":
        data = g.conn.execute("SELECT * FROM Supplier where (Supplier_id ='%s')" %(id))
    else:
        data = g.conn.execute("SELECT * FROM Supplier where (company_name ='%s')" %(id))
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Supplier_information.html",tophat = tophat,name="Supplier")
    

@app.route('/Supply_list')
def Supply_list():
    data = g.conn.execute("SELECT * FROM Supply_list Order by delivery_date desc")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Supply_list_information.html",filelist = tophat,name = "Supply_list")

@app.route('/Supply_list_detail/<list_id>',methods=['POST','GET'])
def Supply_list_detail(list_id):
    
    data = g.conn.execute("SELECT * FROM Item where list_id = '%s'"%(list_id))
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("information.html",tophat = tophat,name = "List ID"+list_id)

@app.route('/Search_Supply_list', methods = ['POST'])
def Search_Supply_list():
    option = request.values.get("option")
    id = request.values.get('supplier_id')
    if not id or not option:
        return render_template("ERROR.html")
    
    if option == "Supplier id":
        data = g.conn.execute("SELECT * FROM Supply_list where (supplier_id ='%s')" %(id))
    else:
        data = g.conn.execute("SELECT * FROM Supply_list where (list_id ='%s')" %(id))
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Supply_list_information.html",filelist = tophat,name="Supply List")

@app.route('/Goods')
def Goods():
    data = g.conn.execute("SELECT * FROM Goods")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Goods.html",tophat = tophat,name="Goods")

@app.route('/Order_')
def Order_():
    data = g.conn.execute("SELECT * FROM Order_ order by order_date desc")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Order_information.html",filelist = tophat,name = "Order")

@app.route('/Search_Order', methods = ['POST'])
def Search_Order():
    id = request.values.get('Order_id')
    if not id:
        return render_template("ERROR.html")
    data = g.conn.execute("SELECT * FROM Order_ where (order_id ='%s')" %(id))
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Supply_list_information.html",filelist = tophat,name="Supply List")

@app.route('/Order_detail/<Order_id>',methods=['POST','GET'])
def Order_detail(Order_id):
    
    data = g.conn.execute("SELECT * FROM Order_item_take_out where order_id = '%s'"%(Order_id))
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    
    
    member_id = g.conn.execute("SELECT member_id FROM buy where order_id = '%s'"%(Order_id))
    if member_id == None:
        memb = None
    else:
        data = g.conn.execute("SELECT * FROM Member where member_id = (SELECT member_id FROM buy where order_id = '%s')"%(Order_id))
        column_names = data.keys()
        memb = []
        memb.append(column_names)
        for row in data:
            memb.append(row)
    
    data = g.conn.execute("SELECT * FROM Employee where employee_id = (SELECT employee_id FROM operate where order_id = '%s')"%(Order_id))
    column_names = data.keys()
    empl = []
    empl.append(column_names)
    for row in data:
        empl.append(row)
    return render_template("Order_detail.html",tophat = tophat,name = "Order ID"+Order_id,memb=memb,empl = empl )

@app.route('/Member')
def Member():
    data = g.conn.execute("SELECT * FROM Member")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Member_information.html",filelist = tophat,name = "Member")

@app.route('/Member_detail/<member_id>',methods=['POST','GET'])
def Member_detail(member_id):
    
    data = g.conn.execute("SELECT * FROM Order_ where order_id in (Select order_id from buy where member_id = '%s')"%(member_id))
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Order_information.html",filelist = tophat,name = "Member_id:" + member_id)

@app.route('/Search_Member', methods = ['POST'])
def Search_Member():
    option = request.values.get("option")
    id = request.values.get('member_id')
    if not id or not option:
        return render_template("ERROR.html")
    
    if option == "member id":
        data = g.conn.execute("SELECT * FROM Member where (member_id ='%s')" %(id))
    else:
        data = g.conn.execute("SELECT * FROM Member where (member_name ='%s')" %(id))
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Member_information.html",filelist = tophat,name="Member")

@app.route('/Employee')
def Employee():
    data = g.conn.execute("SELECT * FROM Employee")
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Employee_information.html",filelist = tophat,name = "Employee")

@app.route('/Employee_detail/<Employee_id>',methods=['POST','GET'])
def Employee_detail(Employee_id):
    
    data = g.conn.execute("SELECT * FROM Order_ where order_id in (Select order_id from operate where employee_id = '%s')"%(Employee_id))
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Order_information.html",filelist = tophat,name = "Employee_id:" + Employee_id)

@app.route('/Search_Employee', methods = ['POST'])
def Search_Employee():
    option = request.values.get("option")
    id = request.values.get('id')
    if not id or not option:
        return render_template("ERROR.html")
    
    if option == "Employee id":
        data = g.conn.execute("SELECT * FROM Employee where (employee_id ='%s')" %(id))
    else:
        data = g.conn.execute("SELECT * FROM Employee where (employee_name ='%s')" %(id))
    column_names = data.keys()
    tophat = []
    tophat.append(column_names)
    for row in data:
        tophat.append(row)
    return render_template("Employee_information.html",filelist = tophat,name="Employee")

@app.route('/Back')
def Back():
    return redirect('/')



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
