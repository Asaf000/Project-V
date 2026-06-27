"""
------------------------------------------------------------
Project : E-Commerce Web Application
Framework : Flask
Author : Thinkora Labs
------------------------------------------------------------
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

from config import Config

# --------------------------------------------------------
# Extensions
# --------------------------------------------------------

db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()

login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"

# --------------------------------------------------------
# Upload Folder
# --------------------------------------------------------

UPLOAD_FOLDER = "static/uploads"

# --------------------------------------------------------
# User Loader
# --------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))

# --------------------------------------------------------
# Application Factory
# --------------------------------------------------------

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # Initialize Extensions

    db.init_app(app)

    bcrypt.init_app(app)

   csrf.init_app(app)

    migrate.init_app(app, db)

    login_manager.init_app(app)

    # ----------------------------------------------------
    # Create Upload Folder
    # ----------------------------------------------------

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    # ----------------------------------------------------
    # Import Models
    # ----------------------------------------------------

    from models.user import User
    from models.product import Product
    from models.cart import Cart
    from models.order import Order
    from models.order_items import OrderItem

    # ----------------------------------------------------
    # Register Blueprints
    # ----------------------------------------------------

    from routes.auth import auth_bp
    from routes.products import product_bp
    from routes.cart import cart_bp
    from routes.checkout import checkout_bp
    from routes.orders import orders_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)

    app.register_blueprint(product_bp)

    app.register_blueprint(cart_bp)

    app.register_blueprint(checkout_bp)

    app.register_blueprint(orders_bp)

    app.register_blueprint(admin_bp)

    # ----------------------------------------------------
    # Home Route
    # ----------------------------------------------------

    @app.route("/")

    def index():

        from models.product import Product

        latest_products = (
            Product.query
            .order_by(Product.created_at.desc())
            .limit(8)
            .all()
        )

        return render_template(
            "home.html",
            products=latest_products
        )

    # ----------------------------------------------------
    # Context Processor
    # ----------------------------------------------------

    @app.context_processor

    def global_variables():

        from flask_login import current_user

        cart_count = 0

        if current_user.is_authenticated:

            cart_count = Cart.query.filter_by(
                user_id=current_user.id
            ).count()

        return dict(
            cart_count=cart_count
        )

    return app

# --------------------------------------------------------
# Create App Instance
# --------------------------------------------------------

app = create_app()

# ==========================================================
# Error Handlers
# ==========================================================

from flask import render_template
from sqlalchemy.exc import SQLAlchemyError
import logging

@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "404.html",
        title="Page Not Found"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    db.session.rollback()

    return render_template(
        "500.html",
        title="Internal Server Error"
    ), 500


@app.errorhandler(SQLAlchemyError)
def database_error(error):

    db.session.rollback()

    logging.error(error)

    return render_template(
        "500.html",
        title="Database Error"
    ), 500


# ==========================================================
# Jinja Filters
# ==========================================================

@app.template_filter("currency")
def currency(value):

    try:
        return f"₹ {float(value):,.2f}"
    except:
        return value


@app.template_filter("upper")
def upper(value):

    return value.upper()


# ==========================================================
# Before Request
# ==========================================================

from flask import session

@app.before_request
def make_session_permanent():

    session.permanent = True


# ==========================================================
# Context Processor
# ==========================================================

@app.context_processor
def utility_processor():

    import datetime

    return dict(

        current_year=datetime.datetime.now().year

    )


# ==========================================================
# Flask CLI Commands
# ==========================================================

@app.cli.command("create-db")
def create_database():

    """
    Creates all database tables.
    """

    db.create_all()

    print("Database Created Successfully.")


@app.cli.command("drop-db")
def drop_database():

    """
    Drops all database tables.
    """

    db.drop_all()

    print("Database Dropped Successfully.")


@app.cli.command("seed-admin")
def seed_admin():

    """
    Creates default administrator.
    """

    from models.user import User

    admin = User.query.filter_by(
        email="admin@gmail.com"
    ).first()

    if admin:

        print("Admin already exists.")

        return

    password = bcrypt.generate_password_hash(
        "admin123"
    ).decode("utf-8")

    admin = User(

        name="Administrator",

        email="admin@gmail.com",

        password=password,

        role="Admin"

    )

    db.session.add(admin)

    db.session.commit()

    print("Default Admin Created Successfully.")


# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(

    filename="ecommerce.log",

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)


logging.info("Application Started Successfully.")

# ==========================================================
# Application Health Check
# ==========================================================

@app.route("/health")
def health():

    return {
        "status": "running",
        "application": "E-Commerce Web Application",
        "version": "1.0.0"
    }


# ==========================================================
# Application Information
# ==========================================================

@app.context_processor
def app_information():

    return dict(

        APP_NAME="E-Commerce Web Application",

        COMPANY="Thinkora Labs",

        VERSION="1.0.0"

    )


# ==========================================================
# Upload Folder Validation
# ==========================================================

def ensure_upload_directory():

    upload_folder = app.config["UPLOAD_FOLDER"]

    if not os.path.exists(upload_folder):

        os.makedirs(upload_folder)

        logging.info("Upload folder created successfully.")


ensure_upload_directory()


# ==========================================================
# Secret Key Validation
# ==========================================================

if not app.config.get("SECRET_KEY"):

    raise RuntimeError(

        "SECRET_KEY is not configured."

    )


# ==========================================================
# Database Initialization
# ==========================================================

with app.app_context():

    try:

        db.create_all()

        logging.info("Database initialized successfully.")

    except Exception as e:

        logging.error(f"Database initialization failed: {e}")


# ==========================================================
# Application Startup
# ==========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
