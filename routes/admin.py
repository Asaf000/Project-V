"""
----------------------------------------------------------
Admin Routes
E-Commerce Web Application
Thinkora Labs
----------------------------------------------------------
"""

import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from app import db

from models.product import Product
from models.category import Category
from models.order import Order
from models.user import User

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

# ==========================================================
# Admin Access Decorator
# ==========================================================

def admin_required():

    if not current_user.is_authenticated:

        return False

    return current_user.role == "Admin"


# ==========================================================
# Dashboard
# ==========================================================

@admin_bp.route("/dashboard")
@login_required
def dashboard():

    if not admin_required():

        flash(
            "Access Denied.",
            "danger"
        )

        return redirect(
            url_for("product.home")
        )

    total_products = Product.query.count()

    total_users = User.query.count()

    total_orders = Order.query.count()

    pending_orders = Order.query.filter_by(
        status="Pending"
    ).count()

    total_categories = Category.query.count()

    latest_orders = (

        Order.query

        .order_by(

            Order.order_date.desc()

        )

        .limit(5)

        .all()

    )

    return render_template(

        "admin_dashboard.html",

        total_products=total_products,

        total_users=total_users,

        total_orders=total_orders,

        pending_orders=pending_orders,

        total_categories=total_categories,

        latest_orders=latest_orders

    )


# ==========================================================
# Products List
# ==========================================================

@admin_bp.route("/products")
@login_required
def products():

    if not admin_required():

        return redirect(
            url_for("product.home")
        )

    products = Product.query.all()

    return render_template(

        "admin_products.html",

        products=products

    )


# ==========================================================
# Add Product
# ==========================================================

@admin_bp.route(
    "/product/add",
    methods=["GET","POST"]
)
@login_required
def add_product():

    if not admin_required():

        return redirect(
            url_for("product.home")
        )

    categories = Category.query.all()

    if request.method == "POST":

        image = request.files.get("image")

        filename = ""

        if image and image.filename:

            filename = secure_filename(
                image.filename
            )

            image.save(

                os.path.join(

                    current_app.config[
                        "UPLOAD_FOLDER"
                    ],

                    filename

                )

            )

        product = Product(

            category_id=request.form.get(
                "category"
            ),

            name=request.form.get(
                "name"
            ),

            description=request.form.get(
                "description"
            ),

            price=float(
                request.form.get("price")
            ),

            stock=int(
                request.form.get("stock")
            ),

            image=filename

        )

        db.session.add(product)

        db.session.commit()

        flash(

            "Product Added Successfully.",

            "success"

        )

        return redirect(

            url_for(

                "admin.products"

            )

        )

    return render_template(

        "add_product.html",

        categories=categories

    )
# ==========================================================
# Edit Product
# ==========================================================

@admin_bp.route(
    "/product/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_product(id):

    if not admin_required():

        return redirect(
            url_for("product.home")
        )

    product = Product.query.get_or_404(id)

    categories = Category.query.all()

    if request.method == "POST":

        product.category_id = request.form.get(
            "category"
        )

        product.name = request.form.get(
            "name"
        )

        product.description = request.form.get(
            "description"
        )

        product.price = float(
            request.form.get("price")
        )

        product.stock = int(
            request.form.get("stock")
        )

        image = request.files.get("image")

        if image and image.filename:

            filename = secure_filename(
                image.filename
            )

            image.save(

                os.path.join(

                    current_app.config[
                        "UPLOAD_FOLDER"
                    ],

                    filename

                )

            )

            product.image = filename

        db.session.commit()

        flash(

            "Product Updated Successfully.",

            "success"

        )

        return redirect(

            url_for(

                "admin.products"

            )

        )

    return render_template(

        "edit_product.html",

        product=product,

        categories=categories

    )


# ==========================================================
# Delete Product
# ==========================================================

@admin_bp.route(
    "/product/delete/<int:id>"
)
@login_required
def delete_product(id):

    if not admin_required():

        return redirect(
            url_for("product.home")
        )

    product = Product.query.get_or_404(id)

    db.session.delete(product)

    db.session.commit()

    flash(

        "Product Deleted Successfully.",

        "success"

    )

    return redirect(

        url_for(

            "admin.products"

        )

    )


# ==========================================================
# Categories
# ==========================================================

@admin_bp.route("/categories")
@login_required
def categories():

    if not admin_required():

        return redirect(
            url_for("product.home")
        )

    categories = Category.query.all()

    return render_template(

        "categories.html",

        categories=categories

    )


# ==========================================================
# Add Category
# ==========================================================

@admin_bp.route(
    "/category/add",
    methods=["GET","POST"]
)
@login_required
def add_category():

    if not admin_required():

        return redirect(
            url_for("product.home")
        )

    if request.method == "POST":

        category = Category(

            name=request.form.get("name"),

            description=request.form.get(
                "description"
            )

        )

        db.session.add(category)

        db.session.commit()

        flash(

            "Category Added Successfully.",

            "success"

        )

        return redirect(

            url_for(

                "admin.categories"

            )

        )

    return render_template(
        "add_category.html"
    )


# ==========================================================
# Delete Category
# ==========================================================

@admin_bp.route(
    "/category/delete/<int:id>"
)
@login_required
def delete_category(id):

    if not admin_required():

        return redirect(
            url_for("product.home")
        )

    category = Category.query.get_or_404(id)

    db.session.delete(category)

    db.session.commit()

    flash(

        "Category Deleted Successfully.",

        "success"

    )

    return redirect(

        url_for(

            "admin.categories"

        )

    )
    # ==========================================================
# Manage Orders
# ==========================================================

@admin_bp.route("/orders")
@login_required
def orders():

    if not admin_required():
        return redirect(url_for("product.home"))

    orders = (
        Order.query
        .order_by(Order.order_date.desc())
        .all()
    )

    return render_template(
        "admin_orders.html",
        orders=orders
    )


# ==========================================================
# Order Details
# ==========================================================

@admin_bp.route("/order/<int:id>")
@login_required
def order_details(id):

    if not admin_required():
        return redirect(url_for("product.home"))

    order = Order.query.get_or_404(id)

    return render_template(
        "admin_order_details.html",
        order=order
    )


# ==========================================================
# Update Order Status
# ==========================================================

@admin_bp.route(
    "/order/status/<int:id>",
    methods=["POST"]
)
@login_required
def update_order_status(id):

    if not admin_required():
        return redirect(url_for("product.home"))

    order = Order.query.get_or_404(id)

    status = request.form.get("status")

    allowed = [
        "Pending",
        "Confirmed",
        "Packed",
        "Shipped",
        "Out for Delivery",
        "Delivered",
        "Cancelled"
    ]

    if status in allowed:

        order.status = status

        db.session.commit()

        flash(
            "Order status updated successfully.",
            "success"
        )

    else:

        flash(
            "Invalid status selected.",
            "danger"
        )

    return redirect(
        url_for(
            "admin.order_details",
            id=id
        )
    )


# ==========================================================
# Users
# ==========================================================

@admin_bp.route("/users")
@login_required
def users():

    if not admin_required():
        return redirect(url_for("product.home"))

    users = (
        User.query
        .order_by(User.created_at.desc())
        .all()
    )

    return render_template(
        "users.html",
        users=users
    )


# ==========================================================
# Dashboard Analytics
# ==========================================================

@admin_bp.route("/analytics")
@login_required
def analytics():

    if not admin_required():
        return redirect(url_for("product.home"))

    total_sales = (
        db.session.query(
            db.func.sum(Order.total_amount)
        ).scalar() or 0
    )

    delivered = Order.query.filter_by(
        status="Delivered"
    ).count()

    pending = Order.query.filter_by(
        status="Pending"
    ).count()

    shipped = Order.query.filter_by(
        status="Shipped"
    ).count()

    cancelled = Order.query.filter_by(
        status="Cancelled"
    ).count()

    total_products = Product.query.count()

    low_stock = Product.query.filter(
        Product.stock <= 5
    ).count()

    return render_template(

        "analytics.html",

        total_sales=total_sales,

        delivered=delivered,

        pending=pending,

        shipped=shipped,

        cancelled=cancelled,

        total_products=total_products,

        low_stock=low_stock

    )


# ==========================================================
# Inventory
# ==========================================================

@admin_bp.route("/inventory")
@login_required
def inventory():

    if not admin_required():
        return redirect(url_for("product.home"))

    products = (
        Product.query
        .order_by(Product.stock.asc())
        .all()
    )

    return render_template(
        "inventory.html",
        products=products
    )


# ==========================================================
# Delete Order
# ==========================================================

@admin_bp.route("/order/delete/<int:id>")
@login_required
def delete_order(id):

    if not admin_required():
        return redirect(url_for("product.home"))

    order = Order.query.get_or_404(id)

    db.session.delete(order)

    db.session.commit()

    flash(
        "Order deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.orders")
    )


# ==========================================================
# Admin Profile
# ==========================================================

@admin_bp.route("/profile")
@login_required
def profile():

    if not admin_required():
        return redirect(url_for("product.home"))

    return render_template(
        "admin_profile.html",
        admin=current_user
    )


# ==========================================================
# Admin Logout Shortcut
# ==========================================================

@admin_bp.route("/logout")
@login_required
def logout():

    return redirect(
        url_for("auth.logout")
    )


# ==========================================================
# Admin Routes Completed
# ==========================================================
