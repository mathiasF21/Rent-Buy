from flask import Blueprint, render_template

bp = Blueprint('home', __name__, url_prefix="/")

@bp.route('/')
def main_page():
    return render_template('home.html')

@bp.route('/about/')
def about():
    return render_template("about.html")

