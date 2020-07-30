from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # first_name = models.CharField(max_length=45)
    # last_name = models.CharField(max_length=45)
    # email = models.CharField(max_length=45)
    # username = models.CharField(max_length=45)
    bday = models.DateField(null=True)
    # password = models.CharField(max_length=180)
    #my_badges
    #my_trash

# class TrashManager(models.Manager):
#     def basic_validator(self, postData):
#         errors = {}
#         now = datetime.now()
#         if not postData['dateout']:
#             errors["date"]= "A takeout date must be included"
#         else:
#             delta = now - (datetime.strptime(postData['dateout'], "%Y-%m-%d"))
#             delta = delta.days
#             if delta > 500:
#                 errors["too_late"]: "Trash can only be taken out within the week."
#             elif delta < 0:
#                 errors["future"]: "You can only add trash that has already been taken out."
#         if len(postData["full"])==0:
#             errors["bag_fill"] = "You shouldn't throw out an empty bag!"
#         if "trashtype" in postData:
#             if postData["trashtype"]=='Zero Waste Week!':
#                 user = postData['user']
#                 start_of_week = now - timedelta(days=now.weekday())
#                 end_of_week = start_of_week + timedelta(days=6)
#                 allmytrash= Trash.objects.filter(user=user).filter(takeout_date__range=(start_of_week,end_of_week))
#                 if allmytrash:
#                     errors["trashexists"] = "There is already trash entered for this week, so it can't be marked as a zero waste week."
#         elif postData["dateout"]:
#             date = datetime.strptime(postData['dateout'], "%Y-%m-%d")
#             user = User.objects.get(id=postData['userid'])
#             start_of_week = date - timedelta(days=date.weekday())
#             end_of_week = start_of_week + timedelta(days=6)
#             allmytrash= Trash.objects.filter(user=user).filter(takeout_date__range=(start_of_week,end_of_week)).filter(trashtype="Zero Waste Week!")
#             if allmytrash:
#                 errors["zerowaste"]="This week was already marked as a zero waste week."
#         return errors

class Trash(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_trash")
    takeout_date = models.DateField()
    bag_size = models.DecimalField(decimal_places=2, max_digits=6)
    fullness = models.DecimalField(decimal_places=2, max_digits=6)
    weight = models.DecimalField(decimal_places=2, max_digits=6)
    trashtype = models.CharField(max_length=180)
    # objects = TrashManager()
    def __repr__(self):
        return f"Trash, takeout date: {self.takeout_date} from user {self.user}"

class Badge(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_badges")
    badge = models.CharField(max_length=180)
    earned_on = models.DateField()