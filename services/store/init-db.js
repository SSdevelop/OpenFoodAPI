db.auth('root', 'pass')
db = db.getSiblingDB('store')

db.createCollection('information', {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["store_id", "name", "contact_emails", "isOpen", "priceBucket"],
            properties: {
                store_id: {
                    bsonType: "string",
                    uniqueItems: true,
                    description: "Must be unique string and is required"
                },
                name: {
                    bsonType: "string",
                    description: "Must be string and is required"
                },
                contact_emails: {
                    bsonType: "array",
                    description: "Contains contact emails and is required"
                },
                isOpen: {
                    bsonType: "bool",
                    description: "Boolean: True is restaurant is open."
                },
                priceBucket: {
                    bsonType: "string",
                    description: "Required: Tells about the price range."
                }
            }
        }
    }
});
db.createCollection('location', {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["store_id", "address1", "city", "country", "postal_code", "state"],
            properties: {
                store_id: {
                    bsonType: "string",
                    uniqueItems: true,
                    description: "Must be unique string and is required"
                },
                address1: {
                    bsonType: "string",
                    description: "Address Line 1; Required"
                },
                address2: {
                    bsonType: "string",
                    description: "Address Line 2; Optional"
                },
                city: {
                    bsonType: "string",
                    description: "City; Required"
                },
                country: {
                    bsonType: "string",
                    description: "Country Name, Required"
                },
                postal_code: {
                    bsonType: "string",
                    description: "Postal Code, Required"
                },
                state: {
                    bsonType: "string",
                    description: "State of location, Required"
                }
            }
        }
    }
});

db.information.insertOne({
    "store_id": "ecs_ny",
    "name": "East Coast Sushi",
    "contact_emails": ["owner@ecs.com", "admin@ecs.com", "support@ecs.com"],
    "isOpen": true,
    "priceBucket": "$$"
});

db.location.insertOne({
    "store_id": "ecs_ny",
    "address1": "636 W 28th Street",
    "address2": "Floor 3",
    "city": "New York",
    "country": "US",
    "postal_code": "10001",
    "state": "NY",
})