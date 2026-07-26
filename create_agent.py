from app import create_app, db
from app.models import Agent
from werkzeug.security import generate_password_hash


app = create_app()


with app.app_context():

    agent = Agent(
        name="Aung Myo Nyunt",
        email="aungmyonyunt@gmail.com",
        phone="092038682",
        viber="092038682",
        password_hash=generate_password_hash("aung123")
    )

    db.session.add(agent)
    db.session.commit()


    print("Agent created successfully!")