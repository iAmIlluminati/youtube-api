from django.http import HttpResponse
from django.shortcuts import render,redirect
from httplib2 import Response
from pexpect import TIMEOUT

from .serializers import KeysSerializer,FetchedDataSerializer
from .models import Keys
from utils import getPagedFind, insertMany,updateOne,insertOne,respToJSON,findAll, updateMany

import pymongo
import datetime
import time
import uuid
import asyncio
import os
import googleapiclient.discovery



# --------------------------------------------------------------------------------------------------


background_tasks = set()
TIME_DELAY = 15  
#Period of API fetch 


# Converting the fetch values into required format
def filterFetchResult(data):
    items = data['items']
    formattedList = list()
    for item in items:
        # print(item)
        item=dict(item)
        formattedList.append({
            "_id":item["id"]["videoId"],
            "thumbnail": "https://i.ytimg.com/vi/"+item["id"]["videoId"]+"/hqdefault.jpg ",
            "publishedAt":item["snippet"]["publishedAt"],
            "title":item["snippet"]["title"],
            "description":item["snippet"]["description"],
       })
    return formattedList



# Fetch function  that uses google API
async def fetchFromYoutubeAPI():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    print("Fetch Performed")
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAivgYkgvaxuYB4NoXf2HYuBDQ0pFEWnWE"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
    dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=230)
    dateConstrain =str(dt.isoformat())
    request = youtube.search().list(
        part="snippet",
        order="date",
        publishedAfter=dateConstrain,
        q="comedy|football|cricket|hindi|english",
        type="video"
    )
    response = request.execute()    
    serializer = FetchedDataSerializer(filterFetchResult(response), many=False)
    insertMany("videos",serializer.data)
    # print(filterFetchResult(response))
    # for val in filterFetchResult(response):
    #     serializer = FetchedDataSerializer(val, many=False)
    #     print(serializer.data)
    #     insertOne("videos",serializer.data)




# To start the background process
async def fetchAPI(request):
    try:
        task = asyncio.create_task(fetchFromYoutubeAPI())
        # Add task to the set. This creates a strong reference.
        background_tasks.add(task)
        while True:
            await fetchFromYoutubeAPI()
            await asyncio.sleep(TIME_DELAY)
        # task.add_done_callback(background_tasks.discard)
    except:
        print("Error in fetchAPI")
    return redirect("dashboard")

# To stop the background process
def stopAPI(request):
    print(background_tasks)
    background_tasks.cancel()
    return HttpResponse("Hello")

# --------------------------------------------------------------------------------------------------





# DASHBOARD APIS
#Dashboard to query the api
def dashboard(request,page=1):
    PAGESIZE=6
    PAGESORT=pymongo.DESCENDING
    PAGEFILTER={}
    title=""
    sort=0
    try:
        PAGENUM=round(float(page))
        if(PAGENUM<=0):
            PAGENUM=1
    except:
        print("Error in page")
        PAGENUM=1
    
    if(request.GET.get('sort', '')):
        try: 
            PAGESORT = int(request.GET.get('sort', ''))
            if(PAGESORT==0):
                sort=0
                PAGESORT=pymongo.DESCENDING
            else:
                sort=1
                PAGESORT=pymongo.ASCENDING
        except:            
            sort=0    
            PAGESORT=pymongo.DESCENDING
    
    if(request.GET.get('title', '')):
        try: 
            title=request.GET.get('title', '')
            PAGEFILTER = {"title":{ "$regex" :request.GET.get('title', '')}}
        except:
            title=""
            PAGEFILTER={}
    
    videos = getPagedFind("videos",PAGEFILTER,PAGESORT,PAGESIZE,PAGENUM)
    if len(videos)==0 :
        return redirect("/1")
    params={
        "title":title,
        "sort":sort,
        "npage":str(PAGENUM+1)+"?title="+title+"&sort="+str(sort),
        "ppage":str(PAGENUM-1)+"?title="+title+"&sort="+str(sort)
    }
    context ={"videos":videos, "params":params}
    return render(request,"dashboard.html",context)



# ------------------------------------------------------------------------------------------------------


# KEYS PAGE AND ITS ROUTES

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
            # print(serializer.data)
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





