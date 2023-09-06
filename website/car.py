from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired

class Car():
    def __init__(self, name, description, seats_number, bags_number, rent_price, full_price):
        if not isinstance(name, str):
            raise TypeError('Name must be a string')
        if not isinstance(description, str):
            raise TypeError('Description must be a string')
        if not isinstance(seats_number, int):
            raise TypeError('Name must be an integer')
        if not isinstance(bags_number, int):
            raise TypeError('Bag number must be an integer')
        self.rent_price = rent_price
        self.name = name
        self.description = description
        self.seats_number = seats_number
        self.bags_number = bags_number
        self.full_price = full_price
        self.car_id = None
        self.cars_in_stock = None
        
    def __repr__(self):
        return f'User({self.name}, {self.description}, {self.full_price}, {self.rent_price})'
        
    def __str__(self):
        value = f'{self.name}: Rent price: {self.rent_price} | Full_price: {self.full_price}'
        return value
    
    def to_json(self):
        return self.__dict__
    
    @classmethod
    def from_json(cls, car_json):
        if not isinstance(car_json, dict):
            raise TypeError("Expected a dictionary")
        return cls(
            name=car_json.get('name'),
            description=car_json.get('description'),
            seats_number=car_json.get('seats_number'),
            bags_number=car_json.get('bags_number'),
            rent_price=car_json.get('rent_price'),
            full_price=car_json.get('full_price'),
            cars_in_stock=car_json.get('cars_in_stock') 
        )
    
class CarEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    seats_number = IntegerField('Seats Number', validators=[DataRequired()])
    bags_number = IntegerField('Bags Number', validators=[DataRequired()])
    rent_price = FloatField('Rent Price', validators=[DataRequired()])
    full_price = FloatField('Full Price', validators=[DataRequired()])
    cars_in_stock = IntegerField('In Stock', validators=[DataRequired()])
    submit = SubmitField('Submit')
