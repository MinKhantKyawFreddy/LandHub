from app import db
from flask_login import UserMixin
from datetime import datetime


class Agent(UserMixin, db.Model):
    __tablename__ = "agents"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    viber = db.Column(
        db.String(20),
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    properties = db.relationship(
        "Property",
        backref="agent",
        lazy=True
    )


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    agent_id = db.Column(
        db.Integer,
        db.ForeignKey("agents.id"),
        nullable=False
    )

    listing_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    property_type = db.Column(
        db.String(50),
        nullable=False
    )

    price = db.Column(
        db.Integer,
        nullable=False
    )

    price_negotiable = db.Column(
        db.Boolean,
        default=False
    )

    area = db.Column(
        db.Float,
        nullable=False
    )

    area_unit = db.Column(
        db.String(20),
        nullable=False
    )

    township = db.Column(
        db.String(100),
        nullable=False
    )

    address = db.Column(
        db.Text
    )

    description = db.Column(
        db.Text
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    contact_person = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(20),
        default="Draft"
    )

    featured = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    images = db.relationship(
        "PropertyImage",
        backref="property",
        lazy=True,
        cascade="all, delete"
    )


class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    image_path = db.Column(
        db.String(255),
        nullable=False
    )

    display_order = db.Column(
        db.Integer,
        default=1
    )