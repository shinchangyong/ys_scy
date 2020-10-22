from flask import Flask
from flask import request
from flask import render_template
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from flask import abort, redirect, url_for, flash
from flask import session
import time
import math
import os

app = Flask(__name__)
# myweb 데이터베이스 생성
app.config["MONGO_URI"] = "mongodb://localhost:27017/myweb"

# 30분동안 session 유지되는 환경설정(30분간 아무반응이 없으면 session값은 사라진다.)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes = 30)
# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds = 30)

# flash를 사용하게되면 SECRET_KEY 사용해야한다.
app.config["SECRET_KEY"] = "some_key"
mongo = PyMongo(app)

BOARD_IMAGE_PATH = "c:\\study\\images"
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])

app.config["BOARD_IMAGE_PATH"] = BOARD_IMAGE_PATH
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024

if not os.path.exists(app.config["BOARD_IMAGE_PATH"]):
    os.mkdir(app.config["BOARD_IMAGE_PATH"])

# web project에 각 모듈들을 모두 포함시킴
from .common import login_required, allowed_file, rand_generator
from .filter import datetime_format
from . import board
from . import member
from . import main
app.register_blueprint(board.bp)
app.register_blueprint(member.bp)