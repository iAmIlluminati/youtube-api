from django.shortcuts import render
from httplib2 import Response
from .serializers import KeysSerializer
from .models import Keys
from utils import  updateOne,insertOne,respToJSON,findAll, updateMany

import time
import uuid

#Dashboard to query the api
def dashboard(request):
    return render(request,"dashboard.html")




#Form to add multiple Google API keys and
#see which is expired and which isn't
def keys(request):
    #Form Submission on POST
    if(request.method=='POST'):
        seconds = time.time()
        local_time = time.ctime(seconds)
        body_unicode = request.body.decode('utf-8')
        body = respToJSON(body_unicode)
        key = body['key']
        if(key):
            val = Keys(id=uuid.uuid4().hex,key=key,status="unused",time=local_time)
            serializer = KeysSerializer(val, many=False)
            print(serializer.data)
            insertOne("keys",serializer.data)
    
    tokens=findAll("keys",{})
    context ={"tokens":tokens}
    # Tokens to be rendered in keys page it will be {id:,token:,active:}  (active will be either 'current','unused', 'expired' )
    return render(request,"keys.html",context)




def setOneAsCurrent() :
    return updateOne("keys",{"status":"unused"},{"status":"current"})



#for chnaging the keys, picking the current active and chnaging it to expires
#taking a unused one and setting it to current
def changeExpiredKey():
    updateOne("keys",{"status":"current"},{"status":"expired"})
    updateOne("keys",{"status":"unused"},{"status":"current"})
    return {"message" :"Successfully changed the key"}


#Fix the return type
#TODO on reseting the page  is rendered before updating one as current 
def resetKeys(request):
    updateMany("keys",{},{"status":"unused"})
    setOneAsCurrent()
    return Response({"message" :"Successfully reseted"})









#     def setOneAsCurrent() :
#     updateOne("keys",{},{"status":"current"})

# def resetKeys(request):
#     updateMany("keys",{},{"status":"unused"})
#     setOneAsCurrent()
#     print("Resetting here")
#     return {"message" :"Successfully reseted"}