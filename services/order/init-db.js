db.auth('order', 'pass')
db = db.getSiblingDB('order')

db.createCollection('order', {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id", "display_id", "external_reference_id", "type"],
            properties: {
                id: {
                    bsonType: "string",
                    uniqueItems: true,
                    description: "Must be unique string and is required to identify an order"
                },
              display_id: {
                    bsonType: "string",
                    description: "Must be string, should be displayable friendly, and is required"
                },
                external_reference_id: {
                    bsonType: "string",
                    description: "Contains the optional external reference id of the order"
                },
                type: {
                    bsonType: "string",
                    description: "Must be string, contains the value of the type of delivery"
                }
            }
        }
    }
});
