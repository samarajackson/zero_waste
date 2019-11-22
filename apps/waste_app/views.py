from django.shortcuts import render, redirect, HttpResponse
from .models import User, UserManager, Trash, TrashManager, Badge
from django.contrib import messages
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Avg
from decimal import Decimal
import bcrypt, copy

def index(request):
    month = datetime.now().month
    year = datetime.now().year
    # topmonth = Trash.objects.filter(takeout_date__month=month).values('user').annotate(Sum('weight'))
    topmonth = Trash.objects.values('user__username').annotate(Sum('weight')).filter(takeout_date__year=year).filter(takeout_date__month=month)
    topmonth = topmonth.order_by("weight__sum")
    topyear = Trash.objects.raw("Select id, AVG(total) as average, username FROM (select strftime('%m', takeout_date) as Month, user.id as id, user.username, SUM(weight) as total from waste_app_trash trash, waste_app_user user where trash.user_id = user.id group by username, user.id, strftime('%m', takeout_date) )  group by username order by AVG(total) LIMIT 5")
    if "userid" in request.session:
        user = "userid"
    else:
        user= "No"
    context = {
        "topmonth": topmonth, #need to decide what we are passing to the leaderboard w/o login
        "topyear":topyear,
        "user":user
    }
    return render(request, "leaderboard.html", context)

def load_login(request):

    return render(request, "login.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        #if there are any problems with the request then this will list all fo the errors
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/login")
    else:
        first_name = request.POST["first"]
        last = request.POST["last"]
        email = request.POST["email"]
        pw = request.POST["pw"]
        bday = request.POST["bday"]
        username = request.POST["username"]
        pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        user = User.objects.create(
            first=first_name, last=last, email=email, bday=bday, pw=pw_hash, username=username)
        request.session["userid"] = user.id
        return redirect("/dashboard")


def success(request):
    #this loads the user dashboard
    if "userid" in request.session:
        user = User.objects.get(id=request.session["userid"])
        mytrash= Trash.objects.filter(user=user).order_by('takeout_date').reverse()[:5]
        allmytrash= Trash.objects.filter(user=user).order_by('takeout_date')
        # monthlytrash = Trash.objects.filter(user=user).order_by('takeout_date').annotate(month=TruncMonth('takeout_date')).values('month').aggregate(Sum('weight'))
        monthlytrash = {"Jan":None,"Feb":None,"Mar":None,"Apr":None,"May":None,"Jun":None,"Jul":None,"Aug":None,"Sep":None,"Oct":None,"Nov":None,"Dec":None}
        amounts = []
        average=0.00
        count=0
        zerowaste = 0
        badgelist = {}
        for trash in allmytrash:
            if monthlytrash[trash.takeout_date.strftime('%b')] ==None:
                monthlytrash[trash.takeout_date.strftime('%b')] = float(trash.weight)
            else:
                monthlytrash[trash.takeout_date.strftime('%b')]+= float(trash.weight)
            if trash.trashtype == "Zero Waste Week!":
                zerowaste += 1
        for key in monthlytrash:
            if monthlytrash[key]!=None: #only want to count values that aren't 0??? but what if they had 0 waste all month?
                average += monthlytrash[key]
                count+=1
                amounts.append(monthlytrash[key])
            elif monthlytrash[key]==None:
                amounts.append(0.00)
        #after I add everything then we need to get the average and percents etc.
        if count >0:
            average = average/count
            percent = Decimal(((136.4-average)/136.4) *100).quantize(Decimal('0')) #this is the value for the average american's waste output per month
        else:
            percent = 0
        #need to check to change the phrasing of percentages
        if percent > 0:
            percentstring = f"You create {percent}% less trash than the average American."
        elif percent==0:
            percentstring = f"Start tracking your waste to see how you compare to the average American!"
        else: 
            percent = percent *-1
            percentstring = f"You create {percent}% more trash than the average American."
        #now want to set what badges show up on the user's profile
        badges = Badge.objects.filter(user=user).order_by("earned_on").reverse()
        for badge in badges:
            if "First Place" in badge.badge :
                badgelist["<img src='../static/first.png' alt='First Place' width=50 class='m-2'>"] = badge.badge
            elif "Second Place" in badge.badge:
                badgelist["<img src='../static/second.png' alt='Second place' width=50 class='m-2'>"] = badge.badge
            elif "Third Place" in badge.badge:
                badgelist["<img src='../static/third.png' alt='Third place' width=50 class='m-2'>"] = badge.badge
        #also want to add a zero waste badge
        if zerowaste > 0:
            if zerowaste ==1:
                badgelist["<img src='../static/reward.png' alt='Zero Waste Prize' width=50 class='m-2'>"] = f"{zerowaste} Zero Waste Week!"
            else:
                badgelist["<img src='../static/reward.png' alt='Zero Waste Prize' width=50 class='m-2'>"] = f"{zerowaste} Zero Waste Weeks!"
        context = {
            "user": user,
            "mytrash":mytrash,
            "monthlytrash":monthlytrash,
            "amounts":amounts,
            "percent":percentstring,
            "average":average,
            "zerowasteweeks":zero_waste,
            "badges":badgelist
        }
        return render(request, "homepage.html", context)
    else:
        return redirect("/")


def logout(request):
    if "userid" in request.session:
        del request.session["userid"]
    return redirect("/")


def login(request):
    if User.objects.filter(email=request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['pw'].encode(), user.pw.encode()):
            request.session["userid"] = user.id
            return redirect("/dashboard")
        else:
            context = {
                "error": "Password is incorrect."
            }
    else:
        context = {
            "error": "There is no account with that email address."
        }
    return render(request, "login.html", context)

def take_out_trash(request):
    errors = Trash.objects.basic_validator(request.POST)
    fullnessDict = {"Full":1,"Mostly Full":0.75,"Half Full":0.5,"Mostly Empty":0.25}
    sizeDict = {"Small (4gal)":4,"Tall Kitchen (13gal)":13,"Large Trash (30gal)":30}
    weightDict = {"Small (4gal)":4,"Tall Kitchen (13gal)":15,"Large Trash (30gal)":25}
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/trash")
    else:
        user = User.objects.get(id=request.session["userid"])
        full = fullnessDict[request.POST["full"]]
        size = sizeDict[request.POST["bag"]]
        weightmax = weightDict[request.POST["bag"]]
        total = weightmax * full
        date = request.POST["dateout"]
        Trash.objects.create(user=user,takeout_date=date,bag_size=size,fullness=full,weight=total,trashtype="Trashbag")
        return redirect("/dashboard")

def zero_waste(request):
    #this is the button to mark that you did not create any waste this week.
    user = User.objects.get(id=request.session["userid"])
    date = datetime.now().strftime('%Y-%m-%d')
    postData = {
    "user":user,
    "dateout":date,
    "bag":"0",
    "full":"0",
    "weight":"0",
    "trashtype":"Zero Waste Week!" }
    errors = Trash.objects.basic_validator(postData)

    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/trash")
    else:
        trash = Trash.objects.create(user=user,takeout_date=date,bag_size=0,fullness=0,weight=0,trashtype="Zero Waste Week!")
        return redirect("/dashboard")


def trash(request):
    #this is to load the trash page
    #we want to load in the date
    if "userid" in request.session:
        now = datetime.now().strftime('%Y-%m-%d')
        context = {
            "today":now,
            "userid":request.session["userid"]
        }
        return render(request,"takeout.html", context)
    else:
        return redirect("/")

def deltrash(request, trash_id):
    if "userid" in request.session:
        user = User.objects.get(id=request.session["userid"])
        trash = Trash.objects.get(id=trash_id)
        trash.delete()
        return redirect("/dashboard")
    else:
        return redirect("/")


