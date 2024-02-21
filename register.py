from flask import Blueprint, render_template, request

register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input from form
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Do something with the user input (e.g. store in database)
        # ...

        # Redirect user to a success page
        return render_template('pages-login.html')
    else:
        # Display registration form
        return render_template('pages-register.html')
