# 🛒 E-Commerce Web Application

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-green)

A modern **Full Stack E-Commerce Web Application** built using **Flask**, **MySQL**, **Bootstrap**, and **SQLAlchemy**.

The application provides a complete online shopping experience, including authentication, shopping cart, checkout, order management, and an administrative dashboard for managing products and customer orders.

---

# 📌 Features

## 👤 User Features

- User Registration
- Secure Login
- Password Encryption
- Product Catalog
- Product Details
- Product Search
- Category Filtering
- Add to Cart
- Update Cart Quantity
- Remove from Cart
- Checkout
- Order History
- Order Tracking
- Responsive Design

---

## 👨‍💼 Admin Features

- Admin Login
- Dashboard
- Product Management
- Category Management
- Order Management
- Update Order Status
- Inventory Management
- Upload Product Images

---

# 🛠 Technology Stack

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Jinja2 Templates

## Backend

- Python
- Flask
- SQLAlchemy
- Flask Login
- Flask Migrate
- Flask WTF

## Database

- MySQL

---

# 📂 Project Structure

```text
ecommerce-web-application/

│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── models/
├── routes/
├── templates/
├── static/
├── database/
└── screenshots/
```

---

# 🗄 Database Design

The project contains the following database tables.

- Users
- Categories
- Products
- Cart
- Orders
- Order Items

Future versions may include:

- Wishlist
- Reviews
- Coupons
- Payments
- Shipping Details

---

# 🔐 Authentication

The application implements:

- Password Hashing
- Session Management
- Role-Based Access Control
- CSRF Protection

Roles:

- Admin
- User

---

# 🛒 Shopping Flow

Home

↓

Browse Products

↓

Product Details

↓

Add to Cart

↓

Checkout

↓

Order Confirmation

↓

Order Tracking

---

# 👨‍💻 Admin Flow

Admin Login

↓

Dashboard

↓

Manage Products

↓

Manage Categories

↓

Manage Orders

↓

Update Order Status

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ecommerce-web-application.git
```

## Navigate

```bash
cd ecommerce-web-application
```

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Database

Import

```
database/ecommerce.sql
```

into MySQL.

---

## Configure Environment Variables

Create

```
.env
```

```
SECRET_KEY=your_secret_key

DATABASE_URL=mysql+pymysql://root:password@localhost/ecommerce_db
```

---

## Run Application

```bash
python app.py
```

Application runs on

```
http://127.0.0.1:5000
```

---

# 📸 Screenshots

Add screenshots here.

```
screenshots/

home.png

login.png

products.png

cart.png

checkout.png

admin_dashboard.png
```

---

# 📡 API Overview

Authentication

```
POST /register

POST /login

GET /logout
```

Products

```
GET /products

GET /product/<id>

POST /admin/product

PUT /admin/product/<id>

DELETE /admin/product/<id>
```

Cart

```
POST /cart/add

GET /cart

DELETE /cart/remove
```

Orders

```
POST /checkout

GET /orders

GET /order/<id>
```

---

# 📚 Learning Outcomes

This project demonstrates:

- Full Stack Development
- Flask Framework
- SQLAlchemy ORM
- Authentication
- Authorization
- CRUD Operations
- REST APIs
- Database Design
- MVC Architecture
- Image Upload
- Session Management

---

# 🔮 Future Enhancements

- Online Payments
- Razorpay Integration
- Stripe Integration
- Coupons
- Wishlist
- Product Reviews
- Email Notifications
- Invoice PDF
- Admin Analytics Dashboard
- Sales Reports

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Thinkora Labs**

Built with ❤️ using Flask & MySQL.
