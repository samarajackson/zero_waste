from rest_framework import serializers, validators
from .models import User, Trash
import bcrypt, copy
from datetime import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first','last','username','email','bday','pw')
    def validate_first(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("First name should be at least 2 characters")
        return value
    def validate_last(self,value):
        if len(value) < 2:
            raise serializers.ValidationError("Last name should be at least 2 characters")
        return value
    def validate_username(self,value):
        if not value:
            raise serializers.ValidationError("A username must be provided")
        return value
    def validate_bday(self,value):
        if not value:
            raise serializers.ValidationError("Birthday is a required field")
        return value
    def validate_pw(self,value):
        pw = bcrypt.hashpw(value.encode(), bcrypt.gensalt())
        pw = pw.decode()
        return pw
    def validate_bday(self,value):
        now = datetime.now()
        maxdate = now.replace(year=now.year - 13).date()
        if maxdate <= value:
            raise serializers.ValidationError("You must be at least 13 years old to register")
    def validate_email(self,value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("Email address is already in use for an existing account")
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email")
        return value
        
class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trash
        fields = ['user','takeout_date','bag_size','fullness','weight','trashtype']
    def validate_user(self, data):
        print(data)
    def validate(self,data):
        print('called validate')
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        user = data['user']
        if data["trashtype"]=='Zero Waste':
            allmytrash = Trash.objects.filter(user=user).filter(takeout_date__range = (start_of_week,end_of_week)).filter(weight > 0)
            if allmytrash:
                raise serializers.ValidationError("There is already trash entered for this week, so it can't be marked as a zero waste week.")
        elif data["trashtype"] == 'Trashbag':
            allmytrash= Trash.objects.filter(user=user).filter(takeout_date__range=(start_of_week,end_of_week)).filter(trashtype="Zero Waste")
            if allmytrash:
                raise serializers.ValidationError("This week was already marked as a zero waste week.")
        return data
    def validate_takeout_date(self,value):
        print('called this one')
        now = datetime.now().date()
        if not value:
            raise serializers.ValidationError("A takeout date must be included")
        else:
            delta = now - value
            delta = delta.days
            if delta > 500:
                raise serializers.ValidationError("Trash can only be taken out within the week.")
            elif delta < 0:
                raise serializers.ValidationError("You can only add trash that has already been taken out.")
        return value