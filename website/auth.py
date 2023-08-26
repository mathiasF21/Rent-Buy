
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import logout_user, login_user, login_required
from .user import SignupForm, User
from werkzeug.security import generate_password_hash
from .database import Database

db = Database()

auth = Blueprint("auth", __name__, url_prefix='/auth/')

@auth.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if request.method == 'POST':
        if form.password.data != form.confirm.data:
            flash('The password and the confirmation do not match.', category = 'error')
        elif (db.get_user(form.email.data) != None):
            flash("This email is already being used", category='error')
            return render_template("sign_up.html", form=form)
        else:
            hash = generate_password_hash(form.password.data)
            user = User(form.email.data, hash, form.name.data) 
            db.create_user(user)
            userInserted = db.get_user(form.email.data)
            login_user(userInserted, remember=True)
            flash(f'Account created! Welcome {form.name.data}. We give you a gift card of 2000 CAD to rent any car you want!', category='success')
            return redirect(url_for('home.main_page'))  
    return render_template("sign_up.html",form=form)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.main_page"))

