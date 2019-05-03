from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
from flask_scrypt import generate_random_salt, generate_password_hash, check_password_hash

@app.route('/login')
def login():
    return render_template('login.html')

# authenticates logins
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']
    
    # get user's salt from db
    cursor = conn.cursor()
    saltQuery = 'SELECT salt FROM person WHERE username = %s'
    cursor.execute(saltQuery, (username))
    salt = cursor.fetchone()['salt'].encode()

    # hash user's inputted password using scrypt
    # and compare to DB pw hash
    password_hash = generate_password_hash(password, salt)
    loginQuery = 'SELECT * FROM person WHERE username = %s and password = %s'
    cursor.execute(loginQuery, (username, password_hash))

    #stores results in var
    data = cursor.fetchone()
    cursor.close()

    if (data):
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('main', username=session['username']))
    else:
        error = "Invalid login or username/password"
        return render_template('login.html', error=error)
