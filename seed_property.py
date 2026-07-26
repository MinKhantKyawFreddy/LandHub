from app import create_app, db
from app.models import Property

app = create_app()

with app.app_context():

    property = Property(
        agent_id=1,
        listing_code="LH-000001",
        title="1.5 Acres Near CPM Motor",
        property_type="half real estate with owner name",
        price=7500000000,
        price_negotiable=True,
        area=1.5,
        area_unit="Acres",
        city="Mandalay",
        township="Aungchanthar",
        address="Beside CPM Motor Factory,",
        description="Flat land with road access. Will install transformers for electricity on request with additional charges.",
        latitude=22.022320,
        longitude=96.119183,
        contact_person="Aung Myo Nyunt",
        status="Published",
        featured=True
    )

    db.session.add(property)
    db.session.commit()

    print("Property created successfully!")