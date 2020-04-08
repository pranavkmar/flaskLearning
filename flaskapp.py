from flask import Flask, jsonify, request, redirect, url_for, session, render_template, g
import sqlite3
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'thisisasecret'


def connect_db():
    sql = sqlite3.connect('/home/ubuntu/flask-app/data.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def mainHome():
    session.pop('name', None)
    return "<h1>Welcome on the Flask Main Page</h1>"


# @app.route('/<UserName>')
# def dashboard(UserName):
#     return "<h1>Hello {}!</h1>".format(UserName)
@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'User'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return render_template("home.html", name=name, display=False, myList=['one', 'two', 'three', 'four'], listOfDictionaries=[{'name': 'Zack'}, {'name': 'Zoie'}])


@app.route('/query')
def query():
    usrName = request.args.get('uname')
    usrLoc = request.args.get('loc')
    return "<h1>Hi {}, you are from {} and welcome to the neighbourhood Query Page</h1>".format(usrName, usrLoc)


@app.route('/form', methods=['POST', 'GET'])
def theform():
    if request.method == 'GET':
        return render_template("form.html")
    else:
        userName = request.form['uname']
        userLoc = request.form['loc']

        db = get_db()
        db.execute('insert into users (name, location) values (?,?)',[userName,userLoc])
        db.commit()
        #  return "<h1>Hi {}, you are from {} and welcome to the {} Query Page</h1>".format(userName, userLoc, userLoc)
        return redirect(url_for('home', name=userName))


# @app.route('/process', )
# def processfun():
#     userName = request.form['uname']
#     userLoc = request.form['loc']
#     return "<h1>Hi {}, you are from {} and welcome to the {} Query Page</h1>".format(userName, userLoc, userLoc)


@app.route('/json', methods=['POST', 'GET'])
def jsonData():
    mylist = [1, 2, 3, 4]
    if 'name' in session:
        sname = session['name']
    else:
        sname = 'NotinCacheSession'
    return jsonify({'key': 'Value', 'listKey': [1, 2, 3], 'name': sname})


@app.route('/processjson', methods=['POST'])
def processjsondata():
    data = request.get_json()
    namekey = data['name']
    locationKey = data['loc']
    randomListKey = data['randomList']
    return jsonify({'result': 'hurray!', 'name': namekey, 'locationKeyData': locationKey, 'randomKeyInList': randomListKey[2]})


@app.route('/viewDB')
def viewDB():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '''<h1>The ID is {},The Name is {},
    The location is {}.</h1>
    '''.format(results[1]['id'], results[1]['name'], results[1]['location'])


if __name__ == "__main__":
    app.run(port=5000)
