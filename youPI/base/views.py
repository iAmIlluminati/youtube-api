from django.shortcuts import render


#Dashboard to query the api
def dashboard(request):
    return render(request,"dashboard.html")


#Form to add multiple Google API keys and
#see which is expired and which isn't
def keys(request):
    context ={tokens:[]}
    # Tokens to be rendered in keys page it will be {id:,token:,active:}  (active will be either 'current','unused', 'expired' )
    return render(request,"keys.html",context)