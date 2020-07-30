from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import User, Trash, Badge
from django.contrib import messages
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Avg
from decimal import Decimal
import bcrypt, copy, json
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .serializers import UserSerializer, TrashSerializer
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed, created, or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TrashViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trash to be viewed, created, or edited.
    """
    queryset = Trash.objects.all()
    serializer_class = TrashSerializer
    def create(self, request,*args, **kwargs):
        request.data['user'] = request.COOKIES["userid"]
        print('userid is: ')
        print(request.COOKIES['userid'])
        return super().create(request, *args, **kwargs)

class MonthlyLeaderboardView(views.APIView):
    def get(self, request, format=None):
        """
        This view returns a list of the top 5 of the rankings for low waste given the month. 
        """
        date = datetime.now()
        month = date.month
        year = date.year
        #Query determines lowest waste users for the current month
        topmonth = (Trash.objects.values('user__username')
            .annotate(Sum('weight')).filter(takeout_date__year=year)
            .filter(takeout_date__month=month)).order_by("weight__sum")[:5]
        return Response(topmonth)

@api_view(['GET'])
def annualLeaderboard(request):
    """
    This view returns a list of the top 5 of the rankings for low waste given the year and month.
    """
    date = datetime.now()
    year = date.year
    topyearlist = []
    #Query determines lowest waste users for the current year
    topyear = Trash.objects.raw(
        """SELECT id AS id, 
            AVG(total) AS average,
            username AS username
        FROM 
            (SELECT STRFTIME('%m', takeout_date) AS Month,
                user.id AS id,
                user.username,
                SUM(weight) AS total
            FROM waste_app_trash trash, waste_app_user user
            WHERE trash.user_id = user.id
            GROUP BY username, user.id, STRFTIME('%m', takeout_date))
    GROUP BY username ORDER BY AVG(total) LIMIT 5""")
    for i in range(len(topyear)):
        topyearlist.append({
            'user__username': topyear[i].username,
            'weight__sum': topyear[i].average
        })
    return JsonResponse(topyearlist, safe=False)

@api_view(['GET'])
def my_dashboard(request):
    """
    This gets all of the data for the logged in user to send for the user's dashboard.
    """
    #this loads the user dashboard
    if "userid" in request.COOKIES:
        # Django ORM Queries...
        user = User.objects.get(id=request.COOKIES["userid"])
        all_my_trash= Trash.objects.filter(user=user).order_by('takeout_date')
        badges = Badge.objects.filter(user=user).order_by("earned_on").reverse()
        
        # variable initializations
        monthlytrash = {"Jan":None,"Feb":None,"Mar":None,"Apr":None,"May":None,"Jun":None,"Jul":None,"Aug":None,"Sep":None,"Oct":None,"Nov":None,"Dec":None}
        amounts = []
        average = 0
        count = 0
        zerowaste = 0
        percent = 0
        trash_list = []
        x = []
        y = []
        
        # data modification
        for trash in all_my_trash:
            all_my_trash_month = trash.takeout_date.strftime('%b')
            trash_list.append({'date': trash.takeout_date, 'size': trash.bag_size, 'weight': trash.weight, 'id':trash.id})
            #This will return only months that have trash recordings in the db.
            if monthlytrash[all_my_trash_month] == None:
                monthlytrash[all_my_trash_month] = float(trash.weight)
            else:
                monthlytrash[all_my_trash_month]+= float(trash.weight)
            if trash.trashtype == "Zero Waste":
                zerowaste += 1
        
        #calculate the average amount per active month
        for month, amount in monthlytrash.items():
            if amount != None: 
                average += monthlytrash[month]
                count += 1
                amounts.append(monthlytrash[month])
            elif amount == None:
                amounts.append(0)
        
        #after I add everything then we need to get the average and percents etc.
        if count > 0: #want to have this check in place because don't want to divide by a 0 if there are no results
            average = average/count
            #this is the value for the average american's waste output per month
            percent = Decimal(((136.4-average)/136.4) *100).quantize(Decimal('0'))
        
        context = {
            "user": user.first,
            "monthlytrash": monthlytrash,
            "amounts": amounts,
            "percent": percent,
            "average": average,
            "zerowasteweeks": zerowaste,
            "mytrash" : trash_list,
            # "badges": badges
        }
        response = JsonResponse(context)
        return response
    else:
        return HttpResponse({"error":"oops"})

@api_view(['POST'])
def login(request):
    """
    This endpoint handles a login from the login page.
    """
    data = request.data
    username = data['email']
    password = data['password']
    context = {}
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        context = {
            "user": { 'first': user.first, 'username': user.username, 'id': user.id }
        }
    else:
        context= {"errors": {'email':"Invalid Credentials"}}
    # if User.objects.filter(email=email):
    #     user = User.objects.get(email=email)
    #     if bcrypt.checkpw(data['pw'].encode(), user.password.encode()):
    #         request.session["userid"] = user.id
    #         request.session.modified = True
    #         request.user = user
    #         context = {
    #             "userid": user.id,
    #             "user": { 'first': user.first, 'username': user.username, 'id': user.id }
    #         }
    #     else:
    #         context = {
    #             "errors": {"pw": "Password is incorrect."}
    #         }
    # else:
    #     context = {
    #         "errors": {"email": "There is no account with that email address."}
    #     }
    request.session.set_test_cookie()
    # print(f"session after login: {request.session.items()}")
    return Response(context)

def logout(request):
    request.session.flush()
    return Response({'logged_out':True})

def get_user_data(request):
    user = {}
    if "userid" in request.session:
        user = User.objects.get(id=request.session["userid"])
    return JsonResponse(user)

def deltrash(request, trash_id):
    if "userid" in request.session:
        user = User.objects.get(id=request.session["userid"])
        trash = Trash.objects.get(id=trash_id)
        trash.delete()
        return redirect("/dashboard")
    else:
        return redirect("/")

def get_csrf(request):
    token = get_token(request)
    print(token)
    return JsonResponse({'token': token})
