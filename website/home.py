from flask import Blueprint, render_template

home = Blueprint('home', __name__, url_prefix="/")

@home.route('/')
def main_page():
    return render_template('home.html')

@home.route('/about/')
def about():
    return render_template("about.html")

