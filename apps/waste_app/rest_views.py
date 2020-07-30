"""
Home for DRF powered REST model APIs
"""
from django.contrib.auth import login
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.waste_app.models import User, Trash
from apps.waste_app.permissions import UserCanEditSelf, IsUser
from apps.waste_app.serializers import UserSerializer, TrashSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed, created, or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserCanEditSelf]

    def perform_create(self, serializer):
        # since we're using this for our registration view, login a user after creating it

        user = serializer.save()
        # login needs request, get it from the serializer context, which is set when called from a viewset
        login(serializer._context["request"], user)


class TrashViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trash to be viewed, created, or edited.
    """

    queryset = Trash.objects.all()
    serializer_class = TrashSerializer
    permission_classes = [IsUser, AllowAny]


