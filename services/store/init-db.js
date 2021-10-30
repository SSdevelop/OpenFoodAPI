db.auth('root', 'pass')
db = db.getSiblingDB('store')

db.createCollection('information');
db.createCollection('location');