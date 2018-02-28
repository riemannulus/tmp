from flask import (
    Blueprint, abort, g, redirect, render_template, request, url_for
)

from ..decorators import use_db
from ..models import User, Matrix
from ..utils import get_ip

matrix = Blueprint(
    'matrix', __name__,
    template_folder='templates',
    static_folder='static',
)


@matrix.route('/')
@use_db
def index():
    ip = get_ip()
    user = g.db.query(User).get(ip)
    if user and user.matrix:
        # TODO: Make these entry points.
        if user.matrix.choice == 'blue':
            return redirect(url_for('.out'))
        elif user.matrix.choice == 'red':
            return redirect(url_for('sky.index'))

    return render_template('matrix/index.html')


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
    matrix = Matrix()
    user.ip = ip
    matrix.choice = color
    user.matrix = matrix
    g.db.add(user)
    g.db.commit()
    return redirect(url_for('.index'))


@matrix.route('/out')
def out():
    return render_template('matrix/out.html')
