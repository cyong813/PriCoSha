import redis
from flask_kvsession import KVSessionExtension
from flask import Flask, render_template, request, session
from flask_session import Session
from simplekv.memory.redisstore import RedisStore
import pymysql.cursors

store = RedisStore(redis.StrictRedis())

app = Flask(__name__)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)

Session(app)
KVSessionExtension(store, app)

conn = pymysql.connect(host='localhost',
						user='root',
						password='',
						db='pricosha',
						charset='utf8mb4',
						cursorclass=pymysql.cursors.DictCursor)
