"""
----------------------------------------------------------
Order Item Model
----------------------------------------------------------
"""

from app import db


class OrderItem(db.Model):

    __tablename__ = "order_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    @property
    def subtotal(self):
        return self.quantity * self.price

    def __repr__(self):
        return (
            f"<OrderItem Order:{self.order_id} "
            f"Product:{self.product_id}>"
        )
