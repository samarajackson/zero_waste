from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed, APIException, NotAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from .models import Trash, Badge
from datetime import datetime
from django.db.models import Sum
from decimal import Decimal

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login as django_login, logout as django_logout


@api_view(["GET"])
@permission_classes([AllowAny])
def monthly_leaderboard(request):
    """
    This view returns a list of the top 5 of the rankings for low waste given the month.
    """
    date = datetime.now()
    month = date.month
    year = date.year
    # Query determines lowest waste users for the current month
    topmonth = (  # todo rename response format keys
        Trash.objects.values("user__username")
        .annotate(Sum("weight"))
        .filter(takeout_date__year=year)
        .filter(takeout_date__month=month)
    ).order_by("weight__sum")[:5]
    return Response(topmonth)


@api_view(["GET"])
@permission_classes([AllowAny])
def annual_leaderboard(request):
    """
    This view returns a list of the top 5 of the rankings for low waste given the year and month.
    """

    # Query determines lowest waste users for the current year
    top_for_year = Trash.objects.raw(
        """
        SELECT id AS id, 
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
        GROUP BY username ORDER BY AVG(total) LIMIT 5
    """
    )
    response_list = []
    for row in top_for_year:
        # todo rename response format keys
        response_list.append(
            {"user__username": row.username, "weight__sum": round(row.average,2)}
        )
    return JsonResponse(response_list, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def my_dashboard(request):
    """
    This gets all of the data for the logged in user to send for the user's dashboard.
    """
    if not request.user.is_authenticated:
        # todo find a way to do this with permission class or fix on the front end, context:
        # options call is not sending the cookie after login so using IsAuthenticated returns a 403
        # and we get a CORS not happy with a non-ok status, but later calls function ok.
        # not ideal, but the workaround end effect is the same
        raise NotAuthenticated()
    all_my_trash = Trash.objects.filter(user=request.user).order_by("takeout_date")
    badges = Badge.objects.filter(user=request.user).order_by("earned_on").reverse()

    # variable initializations
    monthlytrash = {
        "Jan": None,
        "Feb": None,
        "Mar": None,
        "Apr": None,
        "May": None,
        "Jun": None,
        "Jul": None,
        "Aug": None,
        "Sep": None,
        "Oct": None,
        "Nov": None,
        "Dec": None,
    }
    amounts = []
    average = 0
    count = 0
    zerowaste = 0
    percent = 0
    trash_list = []
    check = []
    mybadges = []
    # data modification
    for trash in all_my_trash:
        all_my_trash_month = trash.takeout_date.strftime("%b")
        trash_list.append(
            {
                "date": trash.takeout_date,
                "size": trash.bag_size,
                "weight": trash.weight,
                "id": trash.id,
            }
        )
        # This will return only months that have trash recordings in the db.
        if monthlytrash[all_my_trash_month] == None:
            monthlytrash[all_my_trash_month] = float(trash.weight)
        else:
            monthlytrash[all_my_trash_month] += float(trash.weight)
        if trash.trashtype == "Zero Waste":
            zerowaste += 1

    # calculate the average amount per active month
    for month, amount in monthlytrash.items():
        if amount != None:
            average += monthlytrash[month]
            count += 1
            amounts.append(monthlytrash[month])
            check.append(monthlytrash[month])
        else:
            amounts.append(0)
    for badge in badges:
        mybadge = {
            "text": badge.badge,
            "rank": badge.rank
        }
        mybadges.append(mybadge)
    # after I add everything then we need to get the average and percents etc.
    if (
        count > 0
    ):  # want to have this check in place because don't want to divide by a 0
        # if there are no results
        average = average / count
        # this is the value for the average american's waste output per month
        percent = Decimal(((136.4 - average) / 136.4) * 100).quantize(Decimal("0"))

    context = {
        "user": request.user.first_name,
        "monthlytrash": monthlytrash,
        "amounts": amounts,
        "percent": percent,
        "average": average,
        "zerowasteweeks": zerowaste,
        "mytrash": trash_list,
        "check": check,
        "badges": mybadges
    }
    response = JsonResponse(context)
    return response


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    This endpoint handles a login from the login page.
    """
    data = request.data
    # todo, technically this requires username for login
    email = data["email"]
    password = data["password"]
    # todo change django username field to be username so we don't need both
    user = authenticate(request=request, username=email, password=password)
    if user is None:
        raise AuthenticationFailed(detail="Invalid Credentials")
    django_login(request, user)

    return Response(UserSerializer(user).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def logout(request):
    """log a user out"""
    django_logout(request)
    return Response()
