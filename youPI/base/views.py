from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from httplib2 import Response

from .serializers import KeysSerializer,FetchedDataSerializer
from .models import Keys
from utils import removeOne,findOne,getPagedFind, insertMany,updateOne,insertOne,respToJSON,findAll, updateMany


import pymongo
import datetime
import time
import asyncio
import os
import googleapiclient.discovery
import random
from googleapiclient.errors import HttpError



# --------------------------------------------------------------------------------------------------------
def setOneAsCurrent() :
    return updateOne("keys",{"status":"unused"},{"status":"current"})


# TODO Need to see on why fineOne is not working
# Get the current active key before fetching
def getCurrentKey():
    return findAll("keys",{"status":"current"})[0]["key"]

def removeInvalidKey():
    removeOne("keys",{"status":"current"})
    setOneAsCurrent()

#for chnaging the keys, picking the current active and chnaging it to expires
#taking a unused one and setting it to current
def changeExpiredKey():
    updateOne("keys",{"status":"current"},{"status":"expired"})
    updateOne("keys",{"status":"unused"},{"status":"current"})
    return 



def resetAllKeys():
    updateMany("keys",{},{"status":"unused"})
    setOneAsCurrent()
    return Response({"message" :"Successfully reseted"})


#Fix the return type
#TODO on reseting the page  is rendered before updating one as current 


# --------------------------------------------------------------------------------------------------


background_tasks = set()
TIME_DELAY = 15  
#Period of API fetch 
QUERYLIST =["polimer news","songs","album","comedy","football""cricket","hindi","english"]
 

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
    print("ATTEMPING FETCH")
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY=""
    try:
        DEVELOPER_KEY = getCurrentKey()
    except:
        # Need to see if every key is set as unused, leading to 
        # Out of 2 db calls, only the set as current happens 
        # As there is no current for now
        setOneAsCurrent()
        print("No unused developer key, in database")
        # return    
    # DEVELOPER_KEY ="ENTER THE KEY HERE"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
    dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=230)
    dateConstrain =str(dt.isoformat())
    request = youtube.search().list(
        part="snippet",
        order="date",
        publishedAfter=dateConstrain,
        q=random.choice(QUERYLIST),
        type="video"
    )
    try:
        response = request.execute() 
        # print(response) 
        for val in filterFetchResult(response):
            serializer = FetchedDataSerializer(val, many=False)
            # print(serializer.data)
            insertOne("videos",serializer.data)
        # serializer = FetchedDataSerializer(filterFetchResult(response), many=True)
        # insertMany("videos",serializer.data)
        print(response)
    except HttpError as e:
        response=[]
        # Need to handle this with error message for more accuracy
        # Documentation wasnt clear    
        ec =e.resp.status
        if(ec == 403):
            print(changeExpiredKey())
            print("Quota Over on ",DEVELOPER_KEY)
        else:
            # Remove the invalid key
            removeInvalidKey()
            print("Invalid API Key ",DEVELOPER_KEY)
    except Exception as err:
        print("Youtube API Failed, possible unhandled error :" , err)
    # print(filterFetchResult(response))
    # for val in filterFetchResult(response):
    #     serializer = FetchedDataSerializer(val, many=False)
    #     print(serializer.data)
    #     insertOne("videos",serializer.data)



taskFLAG = 0
FLAG=0
# To start the background process
async def fetchAPI(request):
    global taskFLAG
    global FLAG 
    FLAG =1
    try:
        if not taskFLAG :
            taskFLAG=1
            task = asyncio.create_task(fetchFromYoutubeAPI())
        # Add task to the set. This creates a strong reference.
        # background_tasks.add(task)
        try:    
            while FLAG:
                await fetchFromYoutubeAPI()
                await asyncio.sleep(TIME_DELAY)
            # task.add_done_callback(background_tasks.discard)
        except HttpError as e:
            print(e.resp.status, e.content)
        except Exception as err:
            print("The async call function is down : ",err)        
    except HttpError as e:
        print(e.resp.status, e.content)
    except Exception as err:
        print("The async call function is down : ",err)
    return redirect("dashboard")

# To stop the background process
def stopAPI(request):
    global FLAG 
    FLAG = 0 
    return JsonResponse({ "message" : "Background Fetch Stopped"})

def getAPIState(request):
    global FLAG
    return  JsonResponse({ "message" : str(FLAG)})

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
        v =findAll("videos",{})
        if(len(v)==0):
            print("Here")
            context ={"params":{"npage":"\1","ppage":"\1","page":1}}
            return render(request,"dashboard.html",context)
        return redirect("/1")
   
    params={
        "title":title,
        "sort":sort,
        "npage":str(PAGENUM+1)+"?title="+title+"&sort="+str(sort),
        "ppage":str(PAGENUM-1)+"?title="+title+"&sort="+str(sort),
        "page":PAGENUM,
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
            val = Keys(key=key,status="unused",time=local_time)
            serializer = KeysSerializer(val, many=False)
            # print(serializer.data)
            insertOne("keys",serializer.data)
    
    tokens=findAll("keys",{})
    context ={"tokens":tokens}
    # Tokens to be rendered in keys page it will be {id:,token:,active:}  (active will be either 'current','unused', 'expired' )
    return render(request,"keys.html",context)


def resetKeys(request):
    resetAllKeys()
    return HttpResponse({"message" :"Successfully reseted"})




