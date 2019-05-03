from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn, store
from datetime import timedelta

@app.route('/logout')
def logout():
    session.pop('logged_in', False)
    session.pop('username', None)
    cookie_val = request.cookies.get('session').split(".")[0]
    app.permanent_session_lifetime = timedelta(seconds = 1) # remove instantly from redis
    store.delete(cookie_val)
    return redirect(url_for('main'))
