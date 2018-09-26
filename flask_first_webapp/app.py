# Flask is micro framework for python server side
# Jinja2 comes with it as a template engine
# Main flask file of application
# from flask module import Flask 
from flask import Flask
from flask import render_template
from flask import request # for post request 
from flask import session #in order to use session in app
from flask_session import Session # store session server side more control

import datetime

# I want to create web flask app
app= Flask(__name__)
app.secrete_key='super secrete key'

#app.run(host='0.0.0.0', port="33")
# route is part of URL 
# / default page
# When user goes to / function bellow will be executed
@app.route("/")
def index():
#    return "Hello world!"
    # Inside templates directory is index.html, must be there
    headline= "Hello world!"
    return render_template("index.html", headline=headline)

@app.route("/anel")
def index_anel():
    return "Hello  Anele!"

# get from template <string:name> parameter name
@app.route("/<string:name>")
def hello(name):
    name = name.capitalize()
    return "<h1>Hello, "+name+"</h1>" # f"asdf {name}

@app.route("/bye")
def bye():
    headline= "Good bye!!!"
    return render_template("index.html", headline=headline)

@app.route("/holiday")
def holiday():
    headline="holiday"
    now=datetime.datetime.now()
    # bool var
    holiday=now.month==5 and now.day==1
    return render_template("index.html",headline=headline, holiday=holiday)

@app.route('/anime')
def anime():
    names= ["One piece", "Dragon Ball", "Boruto"]
    return render_template("index.html", names=names)

@app.route("/hello", methods=["GET", "POST"])
def hello_post():
    if request.method == "GET":
        return "Please submit the form instead!";
    name= request.form.get("name")
    return render_template("hello.html", name=name)
"""
Notes:
- Use specifi name of application 'myapp.py' but you 
will need to 'export FLASK_APP=myapp'
- In order to specify host run 'flask run --host='0.0.0.0'
- In order to configure dynamically change, configure flask to work in debug mode
(server will reload itself on code change)
(export FLASK_ENV=development)
"""

"""
Linking the routes
"""
@app.route("/first_page")
def first_page():
    return render_template("first_page.html")
@app.route("/second_page")
def second_page():
    return render_template("second_page.html")

"""
  Sessions
"""

notes= [] # global variable list
@app.route("/notes", methods=["GET","POST"])
def note():
    if session.get("notes") is None:
        session["notes"]=[] # my particalur session to have list of notes
    if request.method== "POST":
        #notes.append(request.form.get("note")) # append variable from form
        note= request.form.get("note")
        session["notes"].append(note)
    return render_template("notes.html", notes=session["notes"])

"""
        M A I N
"""
if __name__=="__main__":
   
    # app.debug= True
    app.config["SESSION_PERMANENT"]= False
    app.config["SESSION_TYPE"]= "filesystem"
    Session().init_app(app)
    #sess.init_app(app)
    app.run(host='0.0.0.0')



"""
    In order to run this instead $flask run --host='0.0.0.0' run
    $python app.py

"""
