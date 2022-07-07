from pymongo import MongoClient
connection_string="mongodb+srv://youtube-api:api-ebutuoy@cluster0.nkhhjii.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client['youtube-api']
db['test'].insert_one({'name':'John'})