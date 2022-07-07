from pymongo import MongoClient
def getDB():
    connection_string="mongodb+srv://youtube-api:api-ebutuoy@cluster0.nkhhjii.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client['youtube-api']
    return db

def getCollection(name):
    return getDB()[name]

def insertOne(name,value):
    getCollection(name).insert_one(value)

def insertMany(name,value):
    getCollection(name).insert_many(value)