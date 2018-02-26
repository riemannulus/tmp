from flask import Blueprint, render_template


sky = Blueprint(
    'sky', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/sky'
)


@sky.route('/')
def index():
    return render_template('sky/index.html')
