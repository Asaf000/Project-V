"""
----------------------------------------------------------
Checkout Routes
E-Commerce Web Application
Thinkora Labs
----------------------------------------------------------
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app import db

from models.cart import Cart
from models.order import Order
from models.order_items import OrderItem

checkout_bp = Blueprint(
    "checkout",
    __name__
)

# ==========================================================
# Checkout Page
# ==========================================================

@checkout_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():

    cart_items = Cart.query.filter_by(
        user_id=current_user.id
    ).all()

    if not cart_items:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("cart.view_cart")
        )

    subtotal = sum(
        item.subtotal
        for item in cart_items
    )

    shipping = 0

    if subtotal < 1000:

        shipping = 100

    grand_total = subtotal + shipping

    if request.method == "POST":

        address = request.form.get(
            "address"
        )

        payment_method = request.form.get(
            "payment_method"
        )

        if not address:

            flash(
                "Shipping address is required.",
                "danger"
            )

            return redirect(
                url_for("checkout.checkout")
            )

        order = Order(

            user_id=current_user.id,

            total_amount=grand_total,

            shipping_address=address,

            payment_method=payment_method,

            status="Pending"

        )

        db.session.add(order)

        db.session.commit()
