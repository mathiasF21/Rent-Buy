CREATE TABLE Users (
    id INT IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(300) NOT NULL,
    user_type INT DEFAULT 2,
    funds decimal DEFAULT 2000 NOT NULL
);

CREATE TABLE Cars_Owned (
    car_id INT,
    user_id INT,
    ownership_type VARCHAR(10),
	nm_days_rented INT,
    FOREIGN KEY (car_id) REFERENCES Cars(car_id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Cars (
    car_id INT IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(700) NOT NULL,
    seats_number INT NOT NULL,
    bags_number INT NOT NULL,
    rent_price DECIMAL(10, 2) NOT NULL,
    full_price DECIMAL(10, 2) NOT NULL,
	cars_in_stock INT DEFAULT 10 NOT NULL
);

CREATE TABLE User_type (
    user_type_id INT IDENTITY PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE
);

-- Insert the user types (admin and member)
INSERT INTO User_type (type_name) VALUES ('admin');
INSERT INTO User_type (type_name) VALUES ('member');

INSERT INTO Cars VALUES('Brabus Convertible','The Smart Brabus Convertible is a sleek and sporty two-seater car that combines the iconic design of the Smart Fortwo Convertible with the high-performance enhancements provided by Brabus, a renowned tuning company. This collaboration results in a compact yet powerful convertible that delivers an exhilarating driving experience.', 2, 2, 50, 30000,10);
INSERT INTO Cars VALUES('Ford Focus','The Ford Focus is a popular compact car that has gained a reputation for its versatility, practicality, and enjoyable driving dynamics. With its stylish design, advanced technology, and range of available trims, the Ford Focus appeals to a wide range of drivers.', 4, 2, 60, 45000,10);
INSERT INTO Cars VALUES('Mercedes-Benz A-Class','The Mercedes-Benz A-Class is a premium compact car that combines elegance, advanced technology, and impressive performance. It serves as an entry point into the Mercedes-Benz lineup, offering a luxurious and comfortable driving experience with a range of modern features.', 4, 3, 65, 53000,10);
INSERT INTO Cars VALUES('Mercedes-Benz G350d','The Mercedes-Benz G350d is a rugged and capable luxury SUV that combines off-road prowess with refined comfort and advanced technology. As part of the iconic G-Class lineup, the G350d offers a blend of off-road capability, luxurious amenities, and a powerful diesel engine.', 4, 4, 90, 70000,10);
INSERT INTO Cars VALUES('Toyota Rav4','The Toyota RAV4 is a popular compact SUV that offers a combination of style, versatility, and reliability. As one of Toyota''s best-selling vehicles, the RAV4 has established itself as a practical and capable choice for individuals and families alike.', 4, 3, 75, 63500,10);
INSERT INTO Cars VALUES('Audi Sedan','Audi sedans are known for their sophisticated design, advanced technology, and exceptional performance. With their sleek profiles, luxurious interiors, and a range of available models, Audi sedans cater to those seeking a combination of style, comfort, and driving dynamics.', 4, 2, 67, 80000,10);
INSERT INTO Cars VALUES('Hyundai Tucson Hybrid','The Hyundai Tucson Hybrid is a hybrid version of the popular compact SUV, offering a combination of fuel efficiency, modern design, and versatile functionality. With its hybrid powertrain, the Tucson Hybrid provides an eco-friendly driving experience without compromising on performance and practicality.', 4, 3, 95, 90000,10);
INSERT INTO Cars VALUES('BMW 3 Series Sedan','The BMW 3 Series Sedan is an iconic luxury compact sedan that combines sportiness, elegance, and cutting-edge technology. Renowned for its dynamic driving experience and sophisticated design, the 3 Series Sedan has been a symbol of driving pleasure and craftsmanship for decades.', 4, 2, 68, 55000,10);







