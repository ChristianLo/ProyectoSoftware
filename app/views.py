from flask import flash, redirect, request, url_for, session

from app import app, templates


@app.route('/')
@templates('index.html')
def index():
    pass


@app.route('/setuser/<user>')
def setuser(user):
    session['user'] = user
    return 'User value set to: {}'.format(session['user'])


@app.route('/getuser')
def getuser():
    try:
        return 'User value was previously set to: {}'.format(session['user'])
    except:
        flash('Error', category='danger')
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
@templates('login.html')
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                        request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in', category='success')
            return redirect(url_for('index'))
    return dict(error=error)
