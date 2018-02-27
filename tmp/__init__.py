import os

from flask import Flask, g
from flask_assets import Environment
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Base
from .matrix import matrix
from .sky import sky


DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
assets = Environment(app)

app.register_blueprint(matrix, url_prefix='/matrix')
app.register_blueprint(sky, url_prefix='/sky')



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
