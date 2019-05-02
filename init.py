from flask import Flask, render_template, request, session, url_for, redirect
from appdef import app
import main, login, logout
import pymysql.cursors
from datetime import timedelta

app.secret_key = 'D7X15LEycA'

def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = 'S3CR3T'
    return session['_csrf_token']

app.add_template_global(name='csrf_token', f=generate_csrf_token)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

if __name__ == "__main__":
    app.run('localhost', 5000, debug = True, ssl_context=('localhost.crt', 'localhost.key'))
