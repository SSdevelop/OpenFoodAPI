from flask_mongoengine import MongoEngine

db = MongoEngine()

class Location(db.EmbeddedDocument):
    address = db.StringField(required=True)
    address_2 = db.StringField(required=True)
    city = db.StringField(required=True)
    country = db.StringField(required=True)
    postal_code = db.StringField(required=True)
    state = db.StringField(required=True)
    latitude = db.FloatField(required=True)
    longitude = db.FloatField(required=True)

    meta = {
        'collection': 'location'
    }

class Information(db.Document):
    name = db.StringField(required=True)
    location = db.EmbeddedDocumentField(Location, required=True)
    contact_emails = db.ListField(required=True)
    raw_hero_url = db.URLField(required=True)
    price_bucket = db.StringField()
    status = db.BooleanField()

    meta = {
        'collection': 'information'
    }
