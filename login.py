from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

@app2.route('/')
def home():
    return render_template('pages-login.html')

@app2.route('/login', methods=['POST'])
def login():
    # get user input from the form
    username = request.form['username']
    password = request.form['password']

    # check if the username and password match with the stored credentials
    with open('users.txt', 'r') as file:
        users = file.readlines()
    for user in users:
        stored_username, stored_password = user.strip().split(',')
        if username == stored_username and password == stored_password:
            # if the username and password match, set the session and redirect to the dashboard
            session['username'] = username
            return redirect(home.html)

    # if the username and password do not match, show an error message
    error = 'Invalid username or password'
    return render_template('pages-login.html', error=error)

@app2.route('/dashboard')
def dashboard():
    # check if the user is logged in by checking the session
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    else:
        # if the user is not logged in, redirect to the login page
        return redirect(url_for('home'))

@app2.route('/logout')
def logout():
    # remove the session and redirect to the login page
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
