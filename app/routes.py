from flask import Blueprint, render_template, url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/informative')
def informative():
    return render_template('informative.html')