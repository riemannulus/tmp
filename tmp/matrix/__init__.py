from flask import (
    Blueprint, abort, g, redirect, render_template, request, url_for
)

from ..decorators import use_db
from ..models import Matrix
from ..utils import get_user

matrix = Blueprint(
    'matrix', __name__,
    template_folder='templates',
    static_folder='static',
)


@matrix.route('/')
@use_db
def index():
    user = get_user()
    if user and user.matrix:
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

    user = get_user()
    if user.matrix:
        return redirect(url_for('.index'))

    matrix = Matrix()
    matrix.choice = color
    user.matrix = matrix
    g.db.commit()
    return redirect(url_for('.index'))


@matrix.route('/out')
def out():
    return render_template('matrix/out.html')
