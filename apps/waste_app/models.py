from enum import Enum

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save


class User(AbstractUser):
    """
    User model...
    """

    bday = models.DateField(null=False)
    # todo my_badges
    #  todo my_trash


class Trash(models.Model):
    """
    Trash entry for a specific time for given user
    """

    class Type(str, Enum):
        """ trash type values"""

        # indicates this record is recording a zero waste week
        ZERO_WASTE = "Zero Waste"
        # indicates this is recording a trash value
        TRASHBAG = "Trashbag"

        @classmethod
        def choices(cls):
            """return as tuples for choices field"""
            return ((i.name, i.value) for i in cls)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_trash")
    takeout_date = models.DateField()
    bag_size = models.DecimalField(decimal_places=2, max_digits=6)
    fullness = models.DecimalField(decimal_places=2, max_digits=6)
    weight = models.DecimalField(decimal_places=2, max_digits=6)
    trashtype = models.CharField(max_length=180)

    def __repr__(self):
        return f"Trash, takeout date: {self.takeout_date} from user {self.user}"

    @staticmethod
    def pre_save_validation(sender, instance, *args, **kwargs):
        pass


pre_save.connect(Trash.pre_save_validation, sender=Trash)


class Badge(models.Model):
    """
    Badges for users for trash
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_badges")
    badge = models.CharField(max_length=180)
    earned_on = models.DateField()
