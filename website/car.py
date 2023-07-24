from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired,EqualTo, Regexp, Length

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
        
    def __repr__(self):
        return f'User({self.name}, {self.description}, {self.full_price}, {self.rent_price})'
        
    def __str__(self):
        value = f'{self.name}: Rent price: {self.rent_price} | Full_price: {self.full_price}'
        return value
    