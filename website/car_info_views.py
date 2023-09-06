from flask import Blueprint, render_template, request, flash
from .database import Database

db = Database()

bp = Blueprint("info", __name__, url_prefix='/car-information/')

@bp.route('/<string:car_name>/', methods=['GET', 'POST'])
def display_information(car_name):
    try:
        car = db.get_car(car_name)
    except Exception as e:
        flash("Error occurred.", category='error')
    return render_template("carInformation.html", car=car)

@bp.route('/buy/<string:car_name>/<int:user_id>/', methods=['GET', 'POST'])
def buy_car(car_name, user_id):
    try:
        carChosen = db.get_car(car_name)
        user = db.get_user_id(user_id)
        userFunds = user.funds
        if userFunds < carChosen.full_price:
            flash("Oh no! You don't have enough funds to buy this car.", category='error')
            return render_template('carInformation.html', car_name=carChosen.name, car=carChosen)
        else:
            db.buy_car(carChosen.car_id, user_id, carChosen.full_price)
            flash("Congratulations! You can now go pick up your new car.", category='success')
    except Exception as e:
        flash("Error occurred.", category='error')
    return render_template('carInformation.html', car_name=carChosen.name, car=carChosen)

@bp.route('/rent/<string:car_name>/<int:user_id>/', methods=['GET','POST'])
def rent_car(car_name, user_id):
    try:
        carChosen = db.get_car(car_name)
        user = db.get_user_id(user_id)
        userFunds = user.funds
        number_of_days = int(request.args.get('number_of_days'))
        if number_of_days <= 0:
            flash("It cannot be zero or a negative number", category='error')
            return render_template('carInformation.html', car_name=carChosen.name, car=carChosen)
        elif userFunds < carChosen.rent_price * number_of_days:
            flash("Oh no! You don't have enough funds to rent this car, try with less days.", category='error')
            return render_template('carInformation.html', car_name=carChosen.name, car=carChosen)
        else:
            db.rent_car(carChosen.car_id,user_id, number_of_days, carChosen.rent_price)
        flash("Congratulations! You can now go pick up the rented car.", category='success')
    except:
        flash("Error occurred.", category='error')
    return render_template('carInformation.html', car_name=carChosen.name, car=carChosen)

@bp.route('/in-stock/')
def display_cars():
    try:
        cars = db.get_cars()
        return render_template('cars_in_stock.html',cars=cars)
    except:
        flash("Not able to diplay cars.", category='error')



