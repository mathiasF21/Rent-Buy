from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user
from website.user import LoginForm
from .database import Database
from werkzeug.security import check_password_hash

db = Database()

bp = Blueprint('sign_in', __name__, url_prefix="/sign_in/")

@bp.route('/', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            user = db.get_user(email)
            if user:
                pwd = form.password.data
                if check_password_hash(user.password, pwd):
                    flash("Logged in successfully!", category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('home.main_page'))
                else:
                    flash("Invalid information", category='error')
                    redirect(url_for('auth.sign_up'))
            else:
                flash("Could not find user", category='error')
                redirect(url_for('auth.sign_up'))
        else:
            flash("Invalid form", category='error')
    return render_template('sign_in.html', form=form)