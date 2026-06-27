"""
----------------------------------------------------------
Product Model
----------------------------------------------------------
"""

from datetime import datetime
from app import db


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id")
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    stock = db.Column(
        db.Integer,
        default=0
    )

    image = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    cart_items = db.relationship(
        "Cart",
        backref="product",
        lazy=True
    )

    order_items = db.relationship(
        "OrderItem",
        backref="product",
        lazy=True
    )

    @property
    def in_stock(self):
        return self.stock > 0

    def __repr__(self):
        return f"<Product {self.name}>"
