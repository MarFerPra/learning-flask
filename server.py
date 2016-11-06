from flask import Flask, request, url_for
from mandelbrot import *
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

def getPassword(username):
    db = shelve.get_shelve('c')
    try:
        value = str(db[str(username)])
    except Exception:
        value = ""
    return value

def setPassword(username, password):
    db = shelve.get_shelve('c')
    db[str(username)] = password
    try:
        value = (password == str(db[str(username)]))
    except Exception:
        value = false
    return value

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
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if flask.request.method == 'GET':
        stylesheet_url = url_for('static',filename='styles.css')
        logo_url = url_for('static', filename='assets/images/web-logo.png')
        flask_url = url_for('static', filename='assets/images/flask-logo.png')
        image_url = url_for('static', filename='assets/images/image.jpg')
        urls = {'stylesheet': stylesheet_url, 'logo': logo_url, 'flask_logo': flask_url , 'image': image_url}
        return env.get_template('signup.html').render(urls = urls)

    elif flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        result = setPassword(username, password)
        if result:
            return "Sign up successful."
        else:
            return "Sign up failed."


@app.route('/')
def index():
    stylesheet_url = url_for('static',filename='styles.css')
    logo_url = url_for('static', filename='assets/images/web-logo.png')
    image_url = url_for('static', filename='assets/images/image.jpg')
    flask_url = url_for('static', filename='assets/images/flask-logo.png')
    urls = {'stylesheet': stylesheet_url, 'logo': logo_url, 'flask_logo': flask_url , 'image': image_url}
    return env.get_template('homepage.html').render(urls = urls)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    stylesheet_url = url_for('static',filename='styles.css')
    logo_url = url_for('static', filename='assets/images/web-logo.png')
    flask_url = url_for('static', filename='assets/images/flask-logo.png')
    image_url = url_for('static', filename='assets/images/image.jpg')
    urls = {'stylesheet': stylesheet_url, 'logo': logo_url, 'flask_logo': flask_url , 'image': image_url}
    return env.get_template('hello.html').render(name=name, urls = urls)


@app.errorhandler(404)
def page_not_found(e):
    stylesheet_url = url_for('static',filename='styles.css')
    logo_url = url_for('static', filename='assets/images/web-logo.png')
    image_url = url_for('static', filename='assets/images/image.jpg')
    flask_url = url_for('static', filename='assets/images/flask-logo.png')
    urls = {'stylesheet': stylesheet_url, 'logo': logo_url, 'flask_logo': flask_url , 'image': image_url}
    return env.get_template('404.html').render(urls = urls), 404


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
