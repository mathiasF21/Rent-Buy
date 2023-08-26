import pyodbc

from website.car import Car
from .user import User

import pyodbc

class Database:

    def __init__(self):
        self.conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                                   "Server=LAPTOP-P0T2A5QJ\SQLEXPRESS;"
                                   "Database=CarsDb;"
                                   "Trusted_Connection=yes;")
        self.cursor = self.conn.cursor()

    def get_user(self, email):
        result = self.cursor.execute('SELECT email, password, name, type, id, funds FROM USERS WHERE email = ?', email)
        for row in result:
            user = User(row[0], row[1], row[2])
            user.member_type = row[3]
            user.id = row[4]
            user.funds = row[5]
            return user
        
    def get_user_id(self, id):
        result = self.cursor.execute('SELECT email, password, name, type, id, funds FROM USERS WHERE id = ?', id)
        for row in result:
            user = User(row[0], row[1], row[2])
            user.member_type = row[3]
            user.id = row[4]
            user.funds = row[5]
            return user

    def update_user_name(self, email, new_name):
        if not isinstance(email, str):
            raise TypeError("Expected a string.")
        self.cursor.execute('UPDATE USERS SET name = ? WHERE email = ?', (new_name, email))
        self.conn.commit()

    def update_user_password(self, email, new_password):
        self.cursor.execute('UPDATE USERS SET password = ? where email = ?', (new_password, email))
        self.conn.commit()

    def update_user_funds(self, email, additional_funds):
        if not isinstance(email, str):
            raise TypeError("Expected a string.")
        self.cursor.execute('UPDATE USERS SET funds = funds + ? WHERE email = ?', (additional_funds, email))
        self.conn.commit()

    def update_user_type(self, email):
        if not isinstance(email, str):
            raise TypeError("Expected a string.")
        self.cursor.execute('UPDATE USERS SET type = ? WHERE email = ?', ('premium', email))
        self.conn.commit()

    def create_user(self, user):
        if not isinstance(user, User):
            raise TypeError("Expected an object of type User.")
        self.cursor.execute('INSERT INTO USERS (email, password, name) VALUES (?, ?, ?)', (user.email, user.password, user.name))
        self.conn.commit()

    def delete_user(self, email):
        if not isinstance(email, str):
            raise TypeError("Expected a string.")
        self.cursor.execute('DELETE FROM USERS WHERE email = ?', (email))
        self.conn.commit()

    def get_car(self, name):
        if not isinstance(name, str):
            raise TypeError("Expected a string.")
        result = self.cursor.execute('SELECT car_id, name, description, seats_number, bags_number, rent_price, full_price FROM Cars WHERE name = ?', (name))
        for row in result:
            car = Car(row[1], row[2], row[3], row[4], row[5], row[6])
            car.car_id = row[0]
            return car
        
    def get_car_id(self, car_id):
        if not isinstance(car_id, int):
            raise TypeError("Expected an integer.")
        result = self.cursor.execute('SELECT car_id, name, description, seats_number, bags_number, rent_price, full_price FROM Cars WHERE car_id = ?', (car_id))
        for row in result:
            car = Car(row[1], row[2], row[3], row[4], row[5], row[6])
            car.car_id = row[0]
            return car
        
    def update_car_ownership(self, car_id, ownership_type):
        if not isinstance(car_id, int):
            raise TypeError("Expected an integer")
        self.cursor.execute('UPDATE Cars_Owned SET ownership_type = ? WHERE car_d = ?', (ownership_type, car_id))
        self.conn.commit()

    def buy_car(self, car_id, user_id, full_price):
        if not isinstance(car_id, int):
            raise TypeError("Expected an integer")
        if not isinstance(user_id, int):
            raise TypeError("Expected an integer")
        self.cursor.execute('UPDATE USERS SET funds = (funds - ?) WHERE id = ?',(full_price, user_id))
        self.cursor.execute('INSERT INTO Cars_Owned (car_id, user_id, ownership_type) VALUES (?, ?, ?)', (car_id, user_id, 'bought'))
        self.conn.commit()

    def rent_car(self, car_id, user_id, number_of_days, rent_price):
        if not isinstance(car_id, int):
            raise TypeError("Expected an integer")
        if not isinstance(user_id, int):
            raise TypeError("Expected an integer")
        if not isinstance(number_of_days, int):
            raise TypeError("Expected an integer")
        self.cursor.execute('UPDATE USERS SET funds = funds - (? * ?) WHERE id = ?', (rent_price, number_of_days, user_id))
        self.cursor.execute('INSERT INTO Cars_Owned (car_id, user_id, ownership_type, nm_days_rented) VALUES (?, ?, ?, ?)', (car_id, user_id, 'rented', number_of_days))
        self.conn.commit()
    
    def get_customer_cars(self, user_id):
        if not isinstance(user_id, int):
            raise TypeError("Expected an integer")
        self.cursor.execute("""
                            SELECT DISTINCT Cars.name AS car_name, Cars_Owned.ownership_type AS ownership_type, nm_days_rented 
                            FROM Cars_Owned
                            INNER JOIN Users ON Cars_Owned.user_id = ?
                            INNER JOIN Cars ON Cars_Owned.car_id = Cars.car_id
                            """, (user_id,))
        return self.cursor.fetchall()
    
    def cancel_rent(self, car_id, user_id, rent_price):
        if not isinstance(car_id, int):
            raise TypeError("Expected an integer")
        if not isinstance(user_id, int):
            raise TypeError("Expected an integer")
        self.cursor.execute('SELECT nm_days_rented FROM Cars_Owned WHERE car_id = ?', (car_id,))
        result = self.cursor.fetchone()
        days_rented = result[0] if result else None
        self.cursor.execute("DELETE FROM Cars_Owned WHERE (car_id = ? AND user_id = ?) AND ownership_type = ?",(car_id,user_id,'rented',))
        self.cursor.execute("UPDATE Users SET funds = funds + (? * ?)", (days_rented, rent_price))
        self.conn.commit()
    
    def sell_car(self, car_id, user_id, full_price):
        if not isinstance(car_id, int):
            raise TypeError("Expected an integer")
        if not isinstance(user_id, int):
            raise TypeError("Expected an integer")
        self.cursor.execute("DELETE FROM Cars_Owned WHERE (car_id = ? AND user_id = ?) AND ownership_type = ?",(car_id,user_id,'bought',))
        self.cursor.execute("UPDATE Users SET funds = funds + ? WHERE id = ?", (full_price, user_id,))
        self.conn.commit()
    
    def extend_rent(self, car_id, user_id, extension_days, rent_price):
        if not isinstance(car_id, int):
            raise TypeError("Expected an integer")
        if not isinstance(user_id, int):
            raise TypeError("Expected an integer")
        if not isinstance(extension_days, int):
            raise TypeError("Expected an integer")
        self.cursor.execute("UPDATE Users SET funds = funds - (? * ?) WHERE id = ?", (rent_price, extension_days, user_id,))
        self.cursor.execute("UPDATE Cars_Owned SET nm_days_rented = nm_days_rented + ? WHERE car_id = ?", (extension_days, car_id,))
        self.conn.commit()
    
    def get_rent_days(self, car_id):
        if not isinstance(car_id, int):
            raise TypeError("Expected an integer")
        self.cursor.execute("SELECT nm_days_rented FROM Cars_Owned WHERE car_id = ?", (car_id,))
        result = self.cursor.fetchone()
        if result is not None:
            days_of_rent = result[0]
            return days_of_rent
        else:
            return None
    
    def close(self):
        self.conn.close()
