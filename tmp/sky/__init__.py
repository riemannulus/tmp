from flask import (
    Blueprint, abort, g, jsonify, render_template, request, url_for
)

from ..decorators import use_db
from ..models import Place, Sky
from ..utils import get_user


sky = Blueprint(
    'sky', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/sky'
)


def is_valid_user(user):
    user = get_user()
    if not user:
        return False

    places = set(Place.query.all())
    user_places = set(user.places)

    if user_places != places:
        return False

    return True


@sky.route('/')
@use_db
def index():
    user = get_user()
    if not is_valid_user(user):
        return abort(403)

    auth_url = url_for('.auth', _external=True)
    return render_template('sky/index.html', auth_url=auth_url)


@sky.route('/auth', methods=['POST'])
@use_db
def auth():
    user = get_user()

    alpha = int(request.form.get('alpha'))
    beta = int(request.form.get('beta'))
    gamma = int(request.form.get('gamma'))

    checked = (
        beta > 140 and
        -10 < gamma < 10
    )

    if not checked:
        return abort(400)

    if user.sky:
        user.sky.checked = True
    else:
        sky = Sky(checked=True)
        user.sky = sky

    g.db.commit()

    return url_for('matrix.index', _external=True)
