from app import create_app
from app.models import Property

app = create_app()

with app.app_context():

    properties = Property.query.all()

    for p in properties:
        print(
            p.listing_code,
            p.title,
            p.township,
            p.price
        )