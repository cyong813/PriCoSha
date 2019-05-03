from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn

@app.route('/logout')
def logout():
    session.pop('logged_in', False)
    session.pop('username', None)
    return redirect(url_for('main'))
