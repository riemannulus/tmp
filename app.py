import os

from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .model import Base, User


DATABASE_URI = os.getenv('DATABASE_URI')

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static/dist',
    template_folder='templates',
)


@app.before_first_request
def initialize():
    global Session
    engine = create_engine(DATABASE_URI)
    Session = scoped_session(sessionmaker(engine))


@app.route('/')
def index():
    return render_template('index.html')
