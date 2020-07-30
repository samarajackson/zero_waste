"""
Home for DRF powered REST model APIs
"""
from rest_framework import viewsets

from apps.waste_app.models import User, Trash
from apps.waste_app.permissions import UserCanEditSelf, IsUser, UserIdMatchesCurrentUser
from apps.waste_app.serializers import UserSerializer, TrashSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed, created, or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserCanEditSelf]


class TrashViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trash to be viewed, created, or edited.
    """

    queryset = Trash.objects.all()
    serializer_class = TrashSerializer
    permission_classes = [UserIdMatchesCurrentUser, IsUser]
