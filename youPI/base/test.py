from pymongo import MongoClient
from .serializers import KeysSerializer
from .models import Keys

connection_string="mongodb+srv://youtube-api:api-ebutuoy@cluster0.nkhhjii.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client['youtube-api']
# db['test'].insert_one({'name':'John'})
x = Keys(key="dfdf",status="used")
serializer = KeysSerializer(x, many=False)
print(serializer.data)
    