from flask import Flask, request, url_for
from jinja2 import Environment, PackageLoader
import flask_login
import flask
from flask import jsonify
from mongoengine import *

connect('database')

env = Environment(loader=PackageLoader(__name__, 'templates'))

app = Flask(__name__)
app.secret_key = 'itsasecret'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class Users(Document):
    name = StringField(max_length=20, required=True, unique=True)
    password = StringField(max_length=10, required=True)


class Restaurants(Document):
    name = StringField(max_length=50, required=True, unique=True)
    description = StringField(max_length=300)
    rating = FloatField(min_value=0, max_value=100)


class User(flask_login.UserMixin):
    pass


def getPassword(username):
    user = Users.objects(name=username).first()
    if(user):
        return user.password
    else:
        return ""


def setPassword(username, password):
    user = Users(name=username, password=password)

    user.save()
    saved_user = Users.objects(name=username).first()

    if(saved_user.password == password):
        return True
    else:
        return False


def createRestaurant(name_val, description_val="", rating_val=0):
    print "HELLO"
    restaurant = Restaurants(name=name_val, description=description_val, rating=rating_val)
    restaurant.save()
    saved_restaurant = Restaurants.objects(name=name_val).first()

    if(saved_restaurant.name == name_val):
        return True
    else:
        return False


def rateRestaurant(name, rating):
    restaurant = Restaurants.objects(name=name).first()
    restaurant.rating += rating
    restaurant.save()


def getRestaurant(name):
    return Restaurants.objects(name=name).first()


def getRestaurantPage(page_number, items_per_page=10):
    offset = (page_number - 1) * items_per_page
    return Restaurants.objects.skip(offset).limit(items_per_page)


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
    return env.get_template('homepage.html').render(current_user=current_user)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    current_user = flask_login.current_user
    return env.get_template('homepage.html').render(current_user=current_user)


@login_manager.unauthorized_handler
def unauthorized_handler():
    current_user = flask_login.current_user
    return env.get_template('404.html').render(current_user=current_user), 404


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    current_user = flask_login.current_user

    if flask.request.method == 'GET':
        return env.get_template('signup.html').render(current_user=current_user)

    elif flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        result = setPassword(username, password)
        if result:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('protected'))
        else:
            return env.get_template('404.html').render(current_user=None), 404


@app.route('/')
def index():
    current_user = flask_login.current_user
    return env.get_template('homepage.html').render(current_user=current_user)


@app.route('/restaurants')
def restaurants():
    current_user = flask_login.current_user
    return env.get_template('restaurants.html').render(current_user=current_user)


@app.route('/create_restaurants', methods=['GET', 'POST'])
def create_restaurants():
    current_user = flask_login.current_user

    if flask.request.method == 'GET':
        return env.get_template('create_restaurants.html').render(current_user=current_user)

    elif flask.request.method == 'POST':

        current_user = flask_login.current_user
        name = flask.request.form['name']
        description = flask.request.form['description'] or ""

        result = createRestaurant(name, description)

        if result:
            return env.get_template('restaurants.html').render(current_user=current_user)
        else:
            return env.get_template('404.html').render(current_user=current_user), 404


@app.route('/get_restaurants', methods=['GET'])
def get_restaurants():
    page_num = flask.request.args.get('page', 0, type=int)
    items_per_page = flask.request.args.get('per', 0, type=int)

    items = getRestaurantPage(page_num, items_per_page)
    return items.to_json()


@app.route('/view_profile')
@flask_login.login_required
def view_profile():
    current_user = flask_login.current_user
    return env.get_template('view_profile.html').render(current_user=current_user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@flask_login.login_required
def edit_profile():
    current_user = flask_login.current_user
    if flask.request.method == 'GET':
        return env.get_template('edit_profile.html').render(current_user=current_user)
    elif flask.request.method == 'POST':
        flask_login.logout_user()
        username = flask.request.form['username']
        password = flask.request.form['password']
        result = setPassword(username, password)
        if result:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('protected'))
        else:
            return env.get_template('404.html').render(current_user=None), 404


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    current_user = flask_login.current_user
    return env.get_template('hello.html').render(name=name, current_user=current_user)


@app.route('/maps')
def maps():
    current_user = flask_login.current_user
    return env.get_template('maps.html').render(current_user=current_user)


@app.errorhandler(404)
def page_not_found(e):
    current_user = flask_login.current_user
    return env.get_template('404.html').render(current_user=current_user), 404
