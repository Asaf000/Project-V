"""
----------------------------------------------------------
Authentication Routes
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
    flash,
    session
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from sqlalchemy.exc import IntegrityError

from app import db, bcrypt

from models.user import User


# ==========================================================
# Blueprint
# ==========================================================

auth_bp = Blueprint(
    "auth",
    __name__
)


# ==========================================================
# Register
# ==========================================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:

        return redirect(url_for("product.home"))

    if request.method == "POST":

        name = request.form.get("name").strip()

        email = request.form.get("email").strip().lower()

        password = request.form.get("password")

        confirm_password = request.form.get("confirm_password")

        # -------------------------
        # Validation
        # -------------------------

        if not name:

            flash(
                "Name is required.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        if not email:

            flash(
                "Email is required.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        if len(password) < 6:

            flash(
                "Password should contain at least 6 characters.",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already exists.",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )

        encrypted_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        user = User(

            name=name,

            email=email,

            password=encrypted_password,

            role="User"

        )

        try:

            db.session.add(user)

            db.session.commit()

            flash(

                "Registration Successful. Please Login.",

                "success"

            )

            return redirect(
                url_for("auth.login")
            )

        except IntegrityError:

            db.session.rollback()

            flash(
                "Unable to register.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

    return render_template(
        "register.html"
    )


# ==========================================================
# Login
# ==========================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.is_admin():

            return redirect(
                url_for("admin.dashboard")
            )

        return redirect(
            url_for("product.home")
        )

    if request.method == "POST":

        email = request.form.get("email").strip().lower()

        password = request.form.get("password")

        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(
            email=email
        ).first()

        if user is None:

            flash(
                "Invalid Email or Password.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        if not bcrypt.check_password_hash(
            user.password,
            password
        ):

            flash(
                "Invalid Email or Password.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        login_user(
            user,
            remember=remember
        )

        session["username"] = user.name

        flash(

            f"Welcome {user.name}!",

            "success"

        )

        next_page = request.args.get("next")

        if next_page:

            return redirect(next_page)

        if user.is_admin():

            return redirect(
                url_for("admin.dashboard")
            )

        return redirect(
            url_for("product.home")
        )

    return render_template(
        "login.html"
    )

# ==========================================================
# Logout
# ==========================================================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    session.clear()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )


# ==========================================================
# Profile
# ==========================================================

@auth_bp.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html",
        user=current_user
    )


# ==========================================================
# Change Password
# ==========================================================

@auth_bp.route(
    "/change-password",
    methods=["GET", "POST"]
)
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form.get(
            "current_password"
        )

        new_password = request.form.get(
            "new_password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )

        if not bcrypt.check_password_hash(
            current_user.password,
            current_password
        ):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return redirect(
                url_for("auth.change_password")
            )

        if new_password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("auth.change_password")
            )

        if len(new_password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "warning"
            )

            return redirect(
                url_for("auth.change_password")
            )

        current_user.password = bcrypt.generate_password_hash(
            new_password
        ).decode("utf-8")

        db.session.commit()

        flash(
            "Password updated successfully.",
            "success"
        )

        return redirect(
            url_for("auth.profile")
        )

    return render_template(
        "change_password.html"
    )


# ==========================================================
# Forgot Password (Placeholder)
# ==========================================================

@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form.get("email")

        user = User.query.filter_by(
            email=email
        ).first()

        if user:

            flash(
                "Password reset functionality can be integrated with email services.",
                "info"
            )

        else:

            flash(
                "No account found with this email.",
                "warning"
            )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "forgot_password.html"
    )


# ==========================================================
# Helper Function
# ==========================================================

def validate_password(password):

    """
    Basic Password Validation
    """

    if len(password) < 6:
        return False

    return True


# ==========================================================
# Unauthorized Handler
# ==========================================================

@auth_bp.app_errorhandler(403)
def forbidden(error):

    return render_template(
        "403.html"
    ), 403


# ==========================================================
# Authentication Routes Completed
# ==========================================================
