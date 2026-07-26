from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from app.models import Agent, Property


main = Blueprint("main", __name__)


@main.route("/")
def home():

    search = request.args.get("search", "").strip()

    query = Property.query.filter_by(
        status="Published"
    )

    if search:

        query = query.filter(
            (Property.title.ilike(f"%{search}%")) |
            (Property.township.ilike(f"%{search}%")) |
            (Property.city.ilike(f"%{search}%")) |
            (Property.listing_code.ilike(f"%{search}%"))
        )

    properties = query.all()

    return render_template(
        "home.html",
        properties=properties,
        search=search
    )


@main.route("/property/<int:property_id>")
def property_detail(property_id):

    property = Property.query.get_or_404(property_id)

    return render_template(
        "property_detail.html",
        property=property
    )


@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        agent = Agent.query.filter_by(email=email).first()

        if agent and check_password_hash(
            agent.password_hash,
            password
        ):
            login_user(agent)

            return redirect(
                url_for("main.dashboard")
            )

        return "Invalid email or password"

    return render_template("login.html")


@main.route("/dashboard")
def dashboard():

    if not current_user.is_authenticated:
        return redirect(
            url_for("main.login")
        )

    return f"Welcome, {current_user.name}"


@main.route("/logout")
def logout():

    logout_user()

    return redirect(
        url_for("main.login")
    )