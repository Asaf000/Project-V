"""
----------------------------------------------------------
User Model
----------------------------------------------------------
"""

from datetime import datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="User"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ----------------------------
    # Relationships
    # ----------------------------

    cart_items = db.relationship(
        "Cart",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    orders = db.relationship(
        "Order",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ----------------------------
    # Helper Methods
    # ----------------------------

    def is_admin(self):
        return self.role == "Admin"

    def __repr__(self):
        return f"<User {self.email}>"
