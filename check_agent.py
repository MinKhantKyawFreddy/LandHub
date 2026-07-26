from app import create_app
from app.models import Agent


app = create_app()


with app.app_context():

    agents = Agent.query.all()

    for agent in agents:
        print(agent.name, agent.email)