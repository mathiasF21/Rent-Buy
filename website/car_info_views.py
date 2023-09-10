from flask import Blueprint, abort, render_template, request, flash
from .database import Database
from .car import Car, CarEditForm, AddCarForm

db = Database()

bp = Blueprint("info", __name__, url_prefix='/Cars/')

@bp.route('/', methods=['GET', 'POST'])
def display_collection():
    try:
        cars = db.get_cars()
        form = AddCarForm()
        if request.method == 'POST' and form.validate_on_submit():
            newCar = Car(form.name.data,form.description.data,form.seats_number.data,form.bags_number.data,form.rent_price.data,form.full_price.data,form.cars_in_stock.data)
            db.add_car(newCar)
            flash(f'Successfully added the car {form.name.data}', category='success')
    except Exception as e:
        flash("Error occurred.", category='error')
    return render_template("cars.html", cars=cars, form=form)

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
        elif carChosen.cars_in_stock <= 0:
            flash("Oh no! There are no more cars in stock.", category='error')
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
        elif carChosen.cars_in_stock <= 0:
            flash("Oh no! There are no more cars in stock.", category='error')
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

@bp.route('/In stock/', methods=['GET','POST'])
def display_cars():
    try:
        cars = db.get_cars()
        return render_template('cars_in_stock.html',cars=cars)
    except:
        flash("Not able to diplay cars.", category='error')

@bp.route('/edit/<string:car_name>/', methods=['GET','POST'])
def edit_car(car_name): 
    try:
        carChosen = db.get_car(car_name)
        form = CarEditForm()
        if request.method == 'POST' and form.validate_on_submit():
            carChanged = Car(car_name,form.description.data,form.seats_number.data,form.bags_number.data,form.rent_price.data,form.full_price.data,form.cars_in_stock.data)
            db.update_car(carChosen.car_id,carChanged)
            flash(f'Successfully updated the car {car_name}', category='success')
        return render_template('edit_car.html',carChosen=carChosen, form=form)
    except Exception as e:
        abort(404)


