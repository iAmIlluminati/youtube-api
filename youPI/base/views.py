from django.shortcuts import render
from django.forms.models import model_to_dict
from .serializers import KeysSerializer
from .models import Keys
from utils import insertOne,respToJSON

import time
import uuid
import json 

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


    context ={"tokens":[]}

    # Tokens to be rendered in keys page it will be {id:,token:,active:}  (active will be either 'current','unused', 'expired' )
    return render(request,"keys.html",context)