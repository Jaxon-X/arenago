

from rest_framework.permissions import BasePermission
from .models import CustomUser
from django.core.cache import cache

class IsOwnerPermissions(BasePermission):
    def has_permisson(self, request, view):
        if not request.user or request.user.is_authenticated:
            return False

        user_id = request.id

        role_key = f"role:{user_id}"
        current_role = cache.get(role_key)

        if current_role in None:
            try:
                user = CustomUser.objects.get(id=user_id)
                user_role = user.role
                cache.set(role_key, user_role, timeout=None)

            except CustomUser.DoesNotExist:
                return False

        return current_role == "owner"






                
