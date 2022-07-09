import pymongo
# db =""
connection_string="mongodb+srv://youtube-api:api-ebutuoy@cluster0.nkhhjii.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client['youtube-api']
# Descending order of time
db["videos"].create_index([('publishedAt',pymongo.DESCENDING)], name="videos_index_desc")
# # Ascending order of time
db["videos"].create_index([('publishedAt',pymongo.ASCENDING)], name="videos_index_asc")


def getDB():
    return db

def getCollection(name):
    return getDB()[name]

def insertOne(name,value):
    getCollection(name).insert_one(value)

def insertMany(name,value):
    for i in value:
        try:
            getCollection(name).insert_one(i)
        except:
            print("Possible duplicate key",i['_id'])

def makeList(values):
    out= []
    for i in values:
        out.append(i)
    return out

def findAll(name,query):
    return makeList(getCollection(name).find(query)) 

def findOne(name,query):
    return makeList(getCollection(name).find_one(query)) 


def getPagedFind(name,query,sortBy,pageSize,pageNum):
    skipValue=(pageNum-1)*pageSize
    return makeList(getCollection(name).find(query).sort("publishedAt",sortBy).skip(skipValue).limit(pageSize))


def updateMany(name,filter,value):
    return getCollection(name).update_many(filter,{"$set":value})

def updateOne(name,filter,value):
    return getCollection(name).update_one(filter,{"$set":value})

def removeOne(name,filter):
    return getCollection(name).delete_one(filter)
# Form response to JSON Convertor
def respToJSON(str):
    pairs =  str.split("&")
    resp=dict()
    for i in pairs :
        field,value=i.split("=")
        resp[field]=value
    return resp
