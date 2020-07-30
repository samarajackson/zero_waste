from rest_framework import serializers
from .models import User, Trash
from datetime import datetime
from datetime import timedelta


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "bday"]

    def validate_bday(self, value):
        now = datetime.now()
        maxdate = now.replace(year=now.year - 13).date()
        if maxdate <= value:
            raise serializers.ValidationError(
                "You must be at least 13 years old to register"
            )
        return value


class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trash
        fields = ["user", "takeout_date", "bag_size", "fullness", "weight", "trashtype"]

    user = serializers.IntegerField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        user = data["user"]
        if data["trashtype"] == "Zero Waste":
            allmytrash = (
                Trash.objects.filter(user=user)
                .filter(takeout_date__range=(start_of_week, end_of_week))
                .filter(weight__gt=0)
            )
            if allmytrash:
                raise serializers.ValidationError(
                    "There is already trash entered for this week, "
                    "so it can't be marked as a zero waste week."
                )
        elif data["trashtype"] == "Trashbag":
            allmytrash = (
                Trash.objects.filter(user=user)
                .filter(takeout_date__range=(start_of_week, end_of_week))
                .filter(trashtype="Zero Waste")
            )
            if allmytrash:
                raise serializers.ValidationError(
                    "This week was already marked as a zero waste week."
                )
        return data

    def validate_takeout_date(self, value):
        now = datetime.now().date()
        if not value:
            raise serializers.ValidationError("A takeout date must be included")
        else:
            delta = now - value
            delta = delta.days
            if delta > 500:
                raise serializers.ValidationError(
                    "Trash can only be taken out within the week."
                )
            elif delta < 0:
                raise serializers.ValidationError(
                    "You can only add trash that has already been taken out."
                )
        return value
