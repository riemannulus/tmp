from functools import wraps

from flask import current_app, g


def use_db(f):

    @wraps(f)
    def wrapped(*args, **kwarg):
        if not hasattr(g, 'db'):
            g.db = current_app.Session()
        return f(*args, **kwarg)

    return wrapped
