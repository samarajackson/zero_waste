from rest_framework import serializers, validators
from .models import User, Trash
import bcrypt, copy
from datetime import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
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
        