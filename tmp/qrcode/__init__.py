from flask import Blueprint, g, redirect, render_template, request, url_for

from ..decorators import use_db
from ..models import Place
from ..utils import get_user

qrcode = Blueprint(
    'qrcode', __name__,
    template_folder='templates',
    static_folder='static'
)


@qrcode.route('/')
@use_db
def index():
    places_all = g.db.query(Place).order_by(Place.code).all()

    user = get_user()

    if set(places_all) == set(user.places):
        return redirect(url_for('sky.index'))

    return render_template(
        'qrcode/index.html',
        places=places_all,
        user=user
    )


@qrcode.route('/auth')
@use_db
def auth():
    user = get_user()
    code = request.args.get('code')

    place = g.db.query(Place).get(code)

    if place and place not in user.places:
        user.places.append(place)
        g.db.commit()

    return redirect(url_for('.index'))
