from flask import (
    Blueprint, abort, g, redirect, render_template, request, url_for
)

from .decorators import use_db
from .models import User
from .utils import get_ip

matrix = Blueprint(
    'matrix', __name__,
    template_folder='templates/matrix'
)


@matrix.route('/')
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


@matrix.route('/choice')
@use_db
def choice():
    color = request.args.get('choice')
    if color not in ('blue', 'red'):
        return abort(400)

    ip = get_ip()

    user = g.db.query(User).get(ip)
    if user:
        return redirect(url_for('.index'))

    user = User()
    user.ip = ip
    user.choice = color
    g.db.add(user)
    g.db.commit()
    return redirect(url_for('.index'))
