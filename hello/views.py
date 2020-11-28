from django.shortcuts import render
from django.http import HttpResponse
import sys
from .models import Greeting ,places
from django.db.models import F
# Create your views here.
sehirler = [
      "Amsterdam",
    "Athens",
    "Barcelona",
    "Berlin",
   "Bratislava",
    "Brussels",
    "Budapest",
    "Copenhagen",
    "Dublin",
    "Edinburgh",
    "Geneva",
    "Hamburg",
    "Helsinki",
    "Krakow",
    "Lisbon",
    "Ljubljana",
    "London",
    "Luxembourg",
    "Lyon",
    "Madrid",
    "Milan",
    "Munich",
    "Oporto",
    "Oslo",
    "Paris",
    "Prague",
    "Rome",
    "Stockholm",
    "Vienna",
    "Warsaw",
    "Zurich"  ]
def index(request):
    # if 'list' in request.POST:

    if request.method == 'POST':
         
        # if request.POST.get("save_home"):
        print("...",file=sys.stderr)
        # return HttpResponse('Hello from Python!') 
    yer = places.objects.filter().order_by("-click","-CommentsAverage","countofcomments")[:20]

    try:

        if request.method == 'GET': 
            city= request.GET["city"]
            rank= int(request.GET["rank"].replace('+',''))
            maxx= len(request.GET["max"])-2
            minn= len(request.GET["min"])-2
            resCount =  int(request.GET["result"]) 
            #formul = click*CommentsAverage/countofcomments/10>=$minrank 
            # *F('CommentsAverage')/F('countofcomments') 
            yer = places.objects.filter(City=city, MINPRICE__gte=minn,MAXPRICE__lte=maxx, click__gte=rank).order_by("-click","-CommentsAverage","countofcomments")[:resCount]
    except: 
        print(NameError,file=sys.stderr) 
    for p in yer:
        p.Cuisine_Style= p.Cuisine_Style.replace('[','')
        p.Cuisine_Style= p.Cuisine_Style.replace(']','')
        p.Cuisine_Style= p.Cuisine_Style.replace('\\','')
        if p.Cuisine_Style=="":
            p.Cuisine_Style="Bilinmiyor"
    return render(request, "index.html",{"cities":sehirler,"places":yer})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
