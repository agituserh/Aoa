# 拓展文件 flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import redis

from flask_redis import FlaskRedis

redis_client = FlaskRedis()

db = SQLAlchemy()
mail = Mail()
redis_db = redis.Redis(host='127.0.0.1',port=6379,db=1)
