"""
----------------------------------------------------------
Order Routes
E-Commerce Web Application
Thinkora Labs
----------------------------------------------------------
"""

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app import db

from models.order import Order

orders_bp = Blueprint(
    "orders",
    __name__
)

# ==========================================================
# My Orders
# ==========================================================

@orders_bp.route("/orders")
@login_required
def my_orders():

    orders = (

        Order.query

        .filter_by(

            user_id=current_user.id

        )

        .order_by(

            Order.order_date.desc()

        )

        .all()

    )

    return render_template(

        "order_history.html",

        orders=orders

    )


# ==========================================================
# Order Details
# ==========================================================

@orders_bp.route("/order/<int:id>")
@login_required
def order_details(id):

    order = Order.query.get_or_404(id)

    if order.user_id != current_user.id:

        flash(

            "Unauthorized access.",

            "danger"

        )

        return redirect(

            url_for("orders.my_orders")

        )

    return render_template(

        "order_details.html",

        order=order

    )


# ==========================================================
# Track Order
# ==========================================================

@orders_bp.route("/track-order/<int:id>")
@login_required
def track_order(id):

    order = Order.query.get_or_404(id)

    if order.user_id != current_user.id:

        flash(

            "Unauthorized access.",

            "danger"

        )

        return redirect(

            url_for("orders.my_orders")

        )

    return render_template(

        "track_order.html",

        order=order

    )
# ==========================================================
# Cancel Order
# ==========================================================

@orders_bp.route("/cancel-order/<int:id>")
@login_required
def cancel_order(id):

    order = Order.query.get_or_404(id)

    if order.user_id != current_user.id:

        flash(

            "Unauthorized access.",

            "danger"

        )

        return redirect(

            url_for("orders.my_orders")

        )

    if order.status != "Pending":

        flash(

            "Only pending orders can be cancelled.",

            "warning"

        )

        return redirect(

            url_for(

                "orders.order_details",

                id=id

            )

        )

    order.status = "Cancelled"

    db.session.commit()

    flash(

        "Order cancelled successfully.",

        "success"

    )

    return redirect(

        url_for(

            "orders.my_orders"

        )

    )


# ==========================================================
# Order Invoice (Placeholder)
# ==========================================================

@orders_bp.route("/invoice/<int:id>")
@login_required
def invoice(id):

    order = Order.query.get_or_404(id)

    if order.user_id != current_user.id:

        flash(

            "Unauthorized access.",

            "danger"

        )

        return redirect(

            url_for("orders.my_orders")

        )

    return render_template(

        "invoice.html",

        order=order

    )


# ==========================================================
# Orders Routes Completed
# ==========================================================
