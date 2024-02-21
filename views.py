from flask import Blueprint, render_template, request
from texting import introText
from data import getAll, get_url, get_subscriber_count

views = Blueprint(__name__, 'views')

number = 1234567890

@views.route('/')
def login():
    return render_template('pages-login.html')

@views.route('/home.html', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        number = request.form['phone-number']
        introText(number)
        
    return render_template('home.html')
    


@views.route('/invest.html')
def invest():
    return render_template('invest.html')
    
@views.route('/template.html', methods=['GET', 'POST'])
def template():
    if request.method == 'POST':
            namee = request.form['searchInput']
            #url = get_url(searchInput)
            url = get_url(namee)
            count = get_subscriber_count(namee)
            getAll(namee)
            twitter_name = namee.replace(' ', '')
            ticker = twitter_name[:4]
            return render_template("template.html", namee=namee, url=url, twitter_name=twitter_name, ticker=ticker, count=count)
    else:
        return render_template('template.html')

@views.route('/about_us.html')
def about():
    return render_template('about_us.html')

@views.route('/charli.html')
def charli():
    return render_template('charli.html')

@views.route('/contact_thank_you.html')
def thank_you():
    return render_template('contact_thank_you.html')

@views.route('/contact.html')
def contact():
    return render_template('contact.html')

@views.route('/deposit.html')
def deposit():
    return render_template('deposit.html')

@views.route('index.html')
def index():
    return render_template('index.html')

@views.route('/justin_bieber.html')
def justin():
    return render_template('justin_bieber.html')

@views.route('/logan_paul.html')
def logan():
    return render_template('logan_paul.html')

@views.route('/mr_beast.html')
def beast():
    return render_template('mr_beast.html')

@views.route('/pages-login.html')
def plogin():
    return render_template('pages-login.html')

@views.route('/pages-register.html')
def preg():
    return render_template('pages-register.html')

@views.route('/pewdiepie.html')
def pdp():
    return render_template('pewdiepie.html')

@views.route('/referrals.html')
def ref():
    return render_template('referrals.html')

@views.route('/the_rock.html')
def rock():
    return render_template('the_rock.html')

@views.route('/users-profile.html')
def userprof():
    return render_template('users-profile.html')
