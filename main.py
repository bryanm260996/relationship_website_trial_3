from flask import Flask, render_template, request, redirect, url_for, session
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')  # Use environment variable for production
PASSCODE = os.environ.get('PASSCODE', '02100501')  # Store passcode securely


## LOGIN ROUTE ##
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_passcode = request.form.get('passcode')
        if entered_passcode == PASSCODE:
            session['authenticated'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Incorrect passcode. Try again.")

    return render_template('login.html')


## LOGOUT ROUTE ##
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))


## PROTECTED ROUTES ##
def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/our_journey')
@login_required
def our_journey():
    return render_template('our_journey.html')


@app.route('/past_trips')
@login_required
def past_trips():
    return render_template('past_trips.html')


@app.route('/bucketlist')
@login_required
def bucketlist():
    return render_template('bucketlist.html')

@app.route('/countdowns')
@login_required
def countdowns():
    return render_template('countdowns.html')

@app.route('/vision_boards')
@login_required
def vision_boards():
    return render_template('vision_boards.html')

@app.route('/marovision')
@login_required
def maro_vision_board():
    return render_template('maro_vision_board.html')

@app.route('/bryanvision')
@login_required
def bryan_vision_board():
    return render_template('bryan_vision_board.html')


## RUN THE APP ##
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Heroku's PORT variable
    app.run(debug=False, host='0.0.0.0', port=port)
