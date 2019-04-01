from rest_framework import permissions
from . import models


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile."""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class PostOwnStatus(permissions.BasePermission):
    """Allow users to update their own status."""

    def has_object_permission(self,request, view, obj):
        """Checks the user is trying to update their own status."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id

class ReviewPer(permissions.BasePermission):
    """If review of post exists return true, else false"""

    def has_permission(self, request, view):
            try:
                query = models.Review.objects.get(post_id= view.kwargs['pid'], pk=view.kwargs['pk'])
                return True
            except models.Review.DoesNotExist:
                return False
class ReviewPostPer(permissions.BasePermission):
    """Returns true, if the post exits"""

    def has_permission(self, request, view):
        obj = models.Post.objects.filter(pk=view.kwargs['pid']).first()
        if obj:
            return True