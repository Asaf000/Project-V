-- ===========================================================
-- E-Commerce Web Application
-- Database Schema
-- Author: Thinkora Labs
-- ===========================================================

DROP DATABASE IF EXISTS ecommerce_db;

CREATE DATABASE ecommerce_db;

USE ecommerce_db;

-- ===========================================================
-- USERS
-- ===========================================================

CREATE TABLE users (

    id INT PRIMARY KEY AUTO_INCREMENT,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(120) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    role ENUM('Admin','User') DEFAULT 'User',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ===========================================================
-- CATEGORIES
-- ===========================================================

CREATE TABLE categories (

    id INT PRIMARY KEY AUTO_INCREMENT,

    name VARCHAR(100) UNIQUE NOT NULL,

    description TEXT

);

-- ===========================================================
-- PRODUCTS
-- ===========================================================

CREATE TABLE products (

    id INT PRIMARY KEY AUTO_INCREMENT,

    category_id INT,

    name VARCHAR(200) NOT NULL,

    description TEXT,

    price DECIMAL(10,2) NOT NULL,

    stock INT DEFAULT 0,

    image VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(category_id)

    REFERENCES categories(id)

    ON DELETE SET NULL

);

-- ===========================================================
-- CART
-- ===========================================================

CREATE TABLE cart (

    id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT NOT NULL,

    product_id INT NOT NULL,

    quantity INT DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)

    REFERENCES users(id)

    ON DELETE CASCADE,

    FOREIGN KEY(product_id)

    REFERENCES products(id)

    ON DELETE CASCADE

);

-- ===========================================================
-- ORDERS
-- ===========================================================

CREATE TABLE orders (

    id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT NOT NULL,

    total_amount DECIMAL(10,2) NOT NULL,

    status ENUM(

        'Pending',

        'Confirmed',

        'Packed',

        'Shipped',

        'Out for Delivery',

        'Delivered',

        'Cancelled'

    ) DEFAULT 'Pending',

    shipping_address TEXT,

    payment_method VARCHAR(50),

    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)

    REFERENCES users(id)

    ON DELETE CASCADE

);

-- ===========================================================
-- ORDER ITEMS
-- ===========================================================

CREATE TABLE order_items (

    id INT PRIMARY KEY AUTO_INCREMENT,

    order_id INT NOT NULL,

    product_id INT NOT NULL,

    quantity INT NOT NULL,

    price DECIMAL(10,2) NOT NULL,

    FOREIGN KEY(order_id)

    REFERENCES orders(id)

    ON DELETE CASCADE,

    FOREIGN KEY(product_id)

    REFERENCES products(id)

);

-- ===========================================================
-- INDEXES
-- ===========================================================

CREATE INDEX idx_user_email

ON users(email);

CREATE INDEX idx_product_name

ON products(name);

CREATE INDEX idx_order_user

ON orders(user_id);

CREATE INDEX idx_cart_user

ON cart(user_id);

-- ===========================================================
-- DEFAULT ADMIN
-- Password: admin123
-- Replace hash after first deployment.
-- ===========================================================

INSERT INTO users(

name,

email,

password,

role

)

VALUES(

'Administrator',

'admin@gmail.com',

'pbkdf2:sha256:600000$replace_with_generated_hash',

'Admin'

);

-- ===========================================================
-- DEFAULT CATEGORIES
-- ===========================================================

INSERT INTO categories(name,description)

VALUES

('Electronics','Electronic Devices'),

('Fashion','Fashion Products'),

('Books','Books & Novels'),

('Home','Home Appliances'),

('Sports','Sports Equipment');

-- ===========================================================
-- SAMPLE PRODUCTS
-- ===========================================================

INSERT INTO products(

category_id,

name,

description,

price,

stock,

image

)

VALUES

(

1,

'Wireless Headphones',

'Bluetooth Noise Cancelling Headphones',

2999.00,

25,

'headphones.jpg'

),

(

2,

'Casual T-Shirt',

'Premium Cotton T-Shirt',

699.00,

100,

'tshirt.jpg'

),

(

3,

'Python Programming',

'Complete Python Programming Guide',

799.00,

50,

'python_book.jpg'

),

(

4,

'Coffee Maker',

'Automatic Coffee Machine',

4999.00,

15,

'coffee.jpg'

),

(

5,

'Football',

'Professional Match Football',

1299.00,

35,

'football.jpg'

);

-- ===========================================================
-- SAMPLE ORDER
-- ===========================================================

INSERT INTO orders(

user_id,

total_amount,

status,

shipping_address,

payment_method

)

VALUES(

1,

2999.00,

'Delivered',

'Thinkora Labs HQ',

'Cash on Delivery'

);

INSERT INTO order_items(

order_id,

product_id,

quantity,

price

)

VALUES(

1,

1,

1,

2999.00

);

-- ===========================================================
-- DATABASE CREATED SUCCESSFULLY
-- ===========================================================
