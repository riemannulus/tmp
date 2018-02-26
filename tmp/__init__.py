import os

from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Base
from .matrix import matrix


DATABASE_URI = os.getenv('DATABASE_URI')

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static/dist',
    template_folder='templates',
)

app.register_blueprint(matrix, url_prefix='/matrix')


@app.before_first_request
def initialize():
    engine = create_engine(DATABASE_URI)
    app.Session = scoped_session(sessionmaker(engine))
    Base.metadata.create_all(engine)
    Base.query = app.Session.query_property()


@app.after_request
def after_request(response):
    if hasattr(g, 'db'):
        g.db.close()

    return response
