from django.shortcuts import render
from .models import Keys
from django.forms.models import model_to_dict
from pymongo import MongoClient
from .serializers import KeysSerializer
from .models import Keys
import time
import uuid

#Dashboard to query the api
def dashboard(request):
    return render(request,"dashboard.html")


#Form to add multiple Google API keys and
#see which is expired and which isn't
def keys(request):
    if(request.method=='POST'):
        seconds = time.time()
        local_time = time.ctime(seconds)
        x = Keys(id=uuid.uuid4().hex,key="dfdf",status="unused",time=local_time)
        serializer = KeysSerializer(x, many=False)
        print(serializer.data)
    context ={"tokens":[]}
    # Tokens to be rendered in keys page it will be {id:,token:,active:}  (active will be either 'current','unused', 'expired' )
    return render(request,"keys.html",context)