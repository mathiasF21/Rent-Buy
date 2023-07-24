from flask import Blueprint, abort, redirect, render_template, request, flash, url_for
from .user import ProfileEdit, ChangePassword
from .database import Database
from werkzeug.security import generate_password_hash    

db = Database()

users = Blueprint('users',__name__,url_prefix='/My_Account/')

@users.route('/<string:email>/')
def show_user(email):
    try:
        currentUser = db.get_user(email)
        cars_rented_bought = db.get_customer_cars(currentUser.id)
        return render_template('userInformation.html', currentUser=currentUser, cars_rented_bought=cars_rented_bought)
    except Exception as e:
        abort(404)

@users.route('/edit/<string:email>/', methods=['GET', 'POST'])
def editUser(email):
    try:
        currentUser = db.get_user(email)
        form = ProfileEdit()
        if request.method == 'POST':
            new_name = form.name.data
            additional_funds = form.funds.data
            db.update_user_name(email, new_name)
            db.update_user_funds(email, additional_funds)
            flash(f'Succefully updated user {currentUser.email}', category='success')
        return render_template('editUser.html', currentUser=currentUser, form=form)
    except Exception as e:
        abort(404)
    
@users.route('/edit/<string:email>/passwordChange/', methods=['GET','POST'])
def edit_user_password(email):
    try:
        userChosen = db.get_user(email)
        form = ChangePassword()
        if request.method == 'POST':
            hash = generate_password_hash(form.password.data)
            db.update_user_password(email,hash)
            flash(f'Successfully updated password for user {email}', category='success')
        return render_template('changePassword.html',userChosen=userChosen, form=form)
    except Exception as e:
        abort(404)

@users.route('/sell/<string:car_name>/<int:user_id>/', methods=['GET','POST'])
def sell_car(car_name, user_id):
    try:
        currentUser = db.get_user_id(user_id)
        car = db.get_car(car_name)
        db.sell_car(car.car_id,user_id, car.full_price)
        flash(f'Successfully sold the car: {car_name}', category='success')
        email = currentUser.email
        return redirect(url_for('users.show_user', email=email))
    except Exception as e:
        abort(404)

@users.route('/cancel/<string:car_name>/<int:user_id>/', methods=['GET','POST'])
def cancel_car(car_name, user_id):
    try:
        currentUser = db.get_user_id(user_id)
        car = db.get_car(car_name)
        db.cancel_rent(car.car_id,user_id, car.rent_price)
        flash(f'Successfully cancelled the rent car: {car_name}', category='success')
        email = currentUser.email
        return redirect(url_for('users.show_user', email=email))
    except Exception as e:
        abort(404)

@users.route('/extend/<string:car_name>/<int:user_id>/', methods=['GET','POST'])
def extend_rent(car_name, user_id): 
    try:
        currentUser = db.get_user_id(user_id)
        car = db.get_car(car_name)
        number_of_days = int(request.args.get('number_of_days'))
        if currentUser.funds < car.rent_price * number_of_days:
            flash("Oh no! You don't have enough funds to rent this this amount of days more, try with less days.", category='error')
        else:
            db.extend_rent(car.car_id,user_id,number_of_days, car.rent_price)
            flash(f'Successfully extended the rent for: {car_name}', category='success')
            email = currentUser.email
            return redirect(url_for('users.show_user', email=email))
    except Exception as e:
        abort(404)
    
