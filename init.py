from flask import Flask, render_template, request, session, url_for, redirect
from appdef import app
import main, login, logout
import pymysql.cursors
from datetime import timedelta
import os

# generate a random secret key for the app
app.secret_key = os.urandom(24)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

if __name__ == "__main__":
    app.run('localhost', 5000, debug = True, ssl_context=('localhost.crt', 'localhost.key'))
