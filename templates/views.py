from flask import Blueprint

views = Blueprint(__name__, 'views')

@views.route('/')
def home():
    return render_template('home.html')


@views.route('/home')
def home2():
    return "home2 page"