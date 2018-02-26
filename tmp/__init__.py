from functools import wraps
import os

from flask import Flask, abort, g, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Base, User


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
    Base.metadata.create_all(engine)
    Base.query = Session.query_property()


def use_db(f):

    @wraps(f)
    def wrapped(*args, **kwarg):
        assert not hasattr(g, 'db')
        g.db = Session()
        return f(*args, **kwarg)

    return wrapped


@app.after_request
def after_request(response):
    if hasattr(g, 'db'):
        g.db.close()

    return response


def get_ip():
    forwarded = request.headers.getlist('X-Forwarded-For')
    if forwarded:
        return forwarded[0]

    return request.remote_addr


@app.route('/')
@use_db
def index():
    ip = get_ip()
    user = g.db.query(User).get(ip)
    if user:
        # TODO: Make these entry points.
        if user.choice == 'blue':
            return redirect('out')
        elif user.choice == 'red':
            return redirect('second')

    return render_template('index.html')


@app.route('/choice')
@use_db
def choice():
    color = request.args.get('choice')
    if color not in ('blue', 'red'):
        return abort(400)

    ip = get_ip()

    user = g.db.query(User).get(ip)
    if user:
        return redirect(url_for('index'))

    user = User()
    user.ip = ip
    user.choice = color
    g.db.add(user)
    g.db.commit()
    return redirect(url_for('index'))
