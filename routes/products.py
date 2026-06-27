"""
----------------------------------------------------------
Product Routes
E-Commerce Web Application
Thinkora Labs
----------------------------------------------------------
"""

from flask import (
    Blueprint,
    render_template,
    request,
    abort
)

from models.product import Product
from models.category import Category

product_bp = Blueprint(
    "product",
    __name__
)

# ==========================================================
# Home
# ==========================================================

@product_bp.route("/")
def home():

    latest_products = (
        Product.query
        .order_by(Product.created_at.desc())
        .limit(8)
        .all()
    )

    categories = Category.query.all()

    return render_template(
        "home.html",
        products=latest_products,
        categories=categories
    )


# ==========================================================
# All Products
# ==========================================================

@product_bp.route("/products")
def products():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    products = Product.query.paginate(
        page=page,
        per_page=12
    )

    categories = Category.query.all()

    return render_template(

        "products.html",

        products=products,

        categories=categories

    )


# ==========================================================
# Product Details
# ==========================================================

@product_bp.route("/product/<int:id>")
def product_details(id):

    product = Product.query.get_or_404(id)

    related_products = (

        Product.query

        .filter(

            Product.category_id == product.category_id,

            Product.id != product.id

        )

        .limit(4)

        .all()

    )

    return render_template(

        "product_details.html",

        product=product,

        related_products=related_products

    )


# ==========================================================
# Category Products
# ==========================================================

@product_bp.route("/category/<int:id>")
def category_products(id):

    category = Category.query.get_or_404(id)

    page = request.args.get(
        "page",
        1,
        type=int
    )

    products = Product.query.filter_by(

        category_id=id

    ).paginate(

        page=page,

        per_page=12

    )

    categories = Category.query.all()

    return render_template(

        "products.html",

        products=products,

        categories=categories,

        current_category=category

    )
    # ==========================================================
# Search Products
# ==========================================================

@product_bp.route("/search")
def search():

    keyword = request.args.get(

        "q",

        ""

    ).strip()

    page = request.args.get(

        "page",

        1,

        type=int

    )

    if keyword:

        products = Product.query.filter(

            Product.name.ilike(

                f"%{keyword}%"

            )

        ).paginate(

            page=page,

            per_page=12

        )

    else:

        products = Product.query.paginate(

            page=page,

            per_page=12

        )

    categories = Category.query.all()

    return render_template(

        "products.html",

        products=products,

        categories=categories,

        keyword=keyword

    )


# ==========================================================
# Featured Products
# ==========================================================

@product_bp.route("/featured")
def featured():

    featured_products = (

        Product.query

        .order_by(Product.stock.desc())

        .limit(10)

        .all()

    )

    return render_template(

        "featured_products.html",

        products=featured_products

    )


# ==========================================================
# Latest Products
# ==========================================================

@product_bp.route("/latest")
def latest():

    latest_products = (

        Product.query

        .order_by(

            Product.created_at.desc()

        )

        .limit(20)

        .all()

    )

    return render_template(

        "latest_products.html",

        products=latest_products

    )


# ==========================================================
# Out Of Stock Products
# ==========================================================

@product_bp.route("/out-of-stock")
def out_of_stock():

    products = Product.query.filter(

        Product.stock <= 0

    ).all()

    return render_template(

        "out_of_stock.html",

        products=products

    )


# ==========================================================
# Products Route Completed
# ==========================================================
