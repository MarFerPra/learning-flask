from flask import Flask, request, url_for
from mandelbrot import *
from dbhandler import *
from jinja2 import Environment, PackageLoader
import flask_login
import flask
from flask.ext import shelve

env = Environment(loader=PackageLoader(__name__, 'templates'))

app = Flask(__name__)
app.secret_key = 'itsasecret'
app.config['SHELVE_FILENAME'] = 'shelve.db'
shelve.init_app(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    user_pass = getPassword(username)
    if user_pass == "":
        return

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user_pass = getPassword(username)
    if user_pass == "":
        return

    user = User()
    user.id = username
    user.is_authenticated = request.form['password'] == user_pass

    return user

@app.route('/login', methods=['POST'])
def login():
    username = flask.request.form['username']
    if flask.request.form['password'] == getPassword(username):
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    current_user = flask_login.current_user
    return env.get_template('homepage.html').render(current_user = current_user)

@app.route('/logout')
def logout():
    flask_login.logout_user()

    current_user = flask_login.current_user

    return env.get_template('homepage.html').render(current_user = current_user)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    current_user = flask_login.current_user

    if flask.request.method == 'GET':
        return env.get_template('signup.html').render(current_user = current_user)

    elif flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        result = setPassword(username, password)
        return env.get_template('homepage.html').render(current_user = current_user)



@app.route('/')
def index():
    current_user = flask_login.current_user
    return env.get_template('homepage.html').render(current_user = current_user)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    current_user = flask_login.current_user
    return env.get_template('hello.html').render(name=name, current_user = current_user)


@app.errorhandler(404)
def page_not_found(e):
    current_user = flask_login.current_user
    return env.get_template('404.html').render(current_user = current_user), 404


@app.route('/mandelbrot')
def mandelbrot():
	x1 = int(request.args.get('x1'))
	y1 = int(request.args.get('y1'))
	x2 = int(request.args.get('x2'))
	y2 = int(request.args.get('y2'))
	width = int(request.args.get('width'))
	it = int(request.args.get('it'))
	fileName = "mandelbrot-" + str(x1) + "_" + str(x2) + "-" + str(
	    x2) + "_" + str(y2) + "-w" + str(width) + "-it" + str(it) + ".png"
	mandelbrotData = {'imageFile': fileName, 'x1': x1,
	    'x2': x2, 'y1': y1, 'y2': y2, 'width': width, 'it': it}
	renderizaMandelbrot(x1, y1, x2, y2, width, it, fileName)
        return env.get_template('mandelbrot.html').render(  mandelbrotData = mandelbrotData )
