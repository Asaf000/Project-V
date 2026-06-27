# ==========================================================
# Remove Cart Item
# ==========================================================

@cart_bp.route("/cart/remove/<int:id>")
@login_required
def remove_cart_item(id):

    cart_item = Cart.query.get_or_404(id)

    db.session.delete(cart_item)

    db.session.commit()

    flash(
        "Item removed from cart.",
        "success"
    )

    return redirect(
        url_for("cart.view_cart")
    )


# ==========================================================
# Clear Cart
# ==========================================================

@cart_bp.route("/cart/clear")
@login_required
def clear_cart():

    Cart.query.filter_by(
        user_id=current_user.id
    ).delete()

    db.session.commit()

    flash(
        "Cart cleared successfully.",
        "success"
    )

    return redirect(
        url_for("cart.view_cart")
    )


# ==========================================================
# Cart Summary
# ==========================================================

@cart_bp.route("/cart/summary")
@login_required
def cart_summary():

    cart_items = Cart.query.filter_by(
        user_id=current_user.id
    ).all()

    subtotal = sum(
        item.subtotal
        for item in cart_items
    )

    shipping = 0

    if subtotal < 1000 and subtotal > 0:

        shipping = 100

    grand_total = subtotal + shipping

    return {

        "items": len(cart_items),

        "subtotal": subtotal,

        "shipping": shipping,

        "grand_total": grand_total

    }


# ==========================================================
# Cart Completed
# ==========================================================
