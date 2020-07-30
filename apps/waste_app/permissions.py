from rest_framework import permissions

from apps.waste_app.models import User


class UserIdMatchesCurrentUser(permissions.BasePermission):
    """
    only allow users to create data for their own user_id/userid
    """

    def has_permission(self, request, view):
        if request.method in {"PUT", "POST"}:
            user_id = request.data.get("userid")
            if not user_id:
                user_id = request.data.get("user_id")
            if user_id and user_id != request.user.id:
                return False
        return True


class IsUser(permissions.BasePermission):
    """
    Only allow user to access their own data
    Make sure user can only access current user's stuff

    Note: this doesn't get called on POSTs
    """

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, "user"):
            raise ValueError(
                "Programming Error: IsUsers can only be used on model with a user col"
            )
        return obj.user.id == request.user.id


class UserCanEditSelf(permissions.BasePermission):
    """
    Object-level permission to only allow users to access their user model

    Note: this doesn't get called on POSTs
    """

    def has_object_permission(self, request, view, obj):

        if not isinstance(obj, User):
            raise ValueError(
                "Programming Error: UserCanEditSelf can only be used on User model "
            )

        return obj.id == request.user.id
