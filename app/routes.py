from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory
)
import os
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from app.models import Agent, Property, PropertyImage
from app import db



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
        property=property,
        images=property.images
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

    properties = Property.query.filter_by(
        agent_id=current_user.id
    ).all()

    return render_template(
        "dashboard.html",
        properties=properties
    )

@main.route("/property/add", methods=["GET", "POST"])
def add_property():

    if not current_user.is_authenticated:
        return redirect(
            url_for("main.login")
        )


    if request.method == "POST":

        new_property = Property(

            agent_id=current_user.id,

            listing_code=request.form["listing_code"],

            title=request.form["title"],

            property_type=request.form["property_type"],

            price=request.form["price"],

            area=request.form["area"],

            area_unit=request.form["area_unit"],

            city=request.form["city"],

            township=request.form["township"],

            address=request.form["address"],

            description=request.form["description"],

            contact_person=request.form["contact_person"],

            status=request.form["status"],

            latitude=request.form["latitude"],

            longitude=request.form["longitude"]

        )


        db.session.add(new_property)

        db.session.commit()

        #Handle images uploads
        images = request.files.getlist("images")

        if images:

            property_folder = os.path.join(
                "uploads",
                "properties",
                str(new_property.id)
            )   

            os.makedirs(
                property_folder,
                exist_ok=True
            )

            for image in images:

                if image.filename:

                    filename = secure_filename(image.filename)

                    image_path = os.path.join(
                        property_folder,
                        filename
                    )

                    image.save(image_path)

                    property_image = PropertyImage(
                        property_id=new_property.id,
                        image_path=image_path
                    )

                    db.session.add(property_image)

            db.session.commit()


        return redirect(
            url_for("main.dashboard")
        )


    return render_template(
        "add_property.html"
    )

@main.route("/property/edit/<int:property_id>", methods=["GET", "POST"])
def edit_property(property_id):

    if not current_user.is_authenticated:
        return redirect(
            url_for("main.login")
        )


    property = Property.query.get_or_404(property_id)


    if property.agent_id != current_user.id:
        return "Unauthorized"


    if request.method == "POST":

        property.title = request.form["title"]

        property.price = request.form["price"]

        property.city = request.form["city"]

        property.township = request.form["township"]

        property.description = request.form["description"]

        property.status = request.form["status"]


        db.session.commit()


        return redirect(
            url_for("main.dashboard")
        )


    return render_template(
        "edit_property.html",
        property=property
    )

@main.route("/uploads/<path:filename>")
def uploaded_file(filename):

    return send_from_directory(
        "uploads",
        filename
    )

@main.route("/logout")
def logout():

    logout_user()

    return redirect(
        url_for("main.login")
    )

@main.route("/setup")
def setup():

    from werkzeug.security import generate_password_hash

    existing_agent = Agent.query.filter_by(
        email="aungmyonyunt@gmail.com"
    ).first()

    if existing_agent:
        return "Account already exists"


    agent = Agent(
        name="Aung Myo Nyunt",
        email="aungmyonyunt@gmail.com",
        phone="092038682",
        viber="092038682",
        password_hash=generate_password_hash("aung123")
    )


    db.session.add(agent)
    db.session.commit()


    return "Account created successfully"