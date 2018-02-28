import os

from flask import Flask, g
from flask_webpack import Webpack
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Base
from .matrix import matrix
from .sky import sky
from .qrcode import qrcode


DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
webpack = Webpack()
app.config.update({
    'WEBPACK_MANIFEST_PATH': '../build/manifest.json',
    'WEBPACK_ASSETS_URL': '/static/',
})
webpack.init_app(app)

app.register_blueprint(matrix, url_prefix='/matrix')
app.register_blueprint(sky, url_prefix='/sky')
app.register_blueprint(qrcode, url_prefix='/qrcode')


@app.before_first_request
def initialize():
    engine = create_engine(DATABASE_URL)
    app.Session = scoped_session(sessionmaker(engine))
    Base.metadata.create_all(engine)
    Base.query = app.Session.query_property()


@app.after_request
def after_request(response):
    if hasattr(g, 'db'):
        g.db.close()

    return response
