from app import create_app, db
from app.models import Agent


app = create_app()


with app.app_context():

    agent = Agent.query.first()

    agent.email = "aungmyonyunt@gmail.com"

    db.session.commit()

    print("Email updated!")