from pymongo import MongoClient

# db =""
connection_string="mongodb+srv://youtube-api:api-ebutuoy@cluster0.nkhhjii.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client['youtube-api']

def getDB():
    return db

def getCollection(name):
    return getDB()[name]

def insertOne(name,value):
    getCollection(name).insert_one(value)

def insertMany(name,value):
    getCollection(name).insert_many(value)

def makeList(values):
    out= []
    for i in values:
        out.append(i)
    return out

def findAll(name,query):
    return makeList(getCollection(name).find(query)) 

def updateMany(name,filter,value):
    return getCollection(name).update_many(filter,{"$set":value})

def updateOne(name,filter,value):
    return getCollection(name).update_one(filter,{"$set":value})


# Form response to JSON Convertor
def respToJSON(str):
    pairs =  str.split("&")
    resp=dict()
    for i in pairs :
        field,value=i.split("=")
        resp[field]=value
    return resp
