from typing import Type
from src.apps.auth.models import User
from src.enums.base import Action, AppModule
from src.utilities.crypto_func import JWTService
from fastapi import Depends
from src.utilities.errorHandler import ErrorMessage


error = ErrorMessage(User)
jwt = JWTService()

class AuthPermissionService:
    @staticmethod
    async def has_permission(user: User, action: Action, module: AppModule) -> bool:
        if user.is_superuser:
            return True

        groups = await user.permission_groups.all().prefetch_related("permissions")
        for group in groups:
            perms = await group.permissions.all()
            for perm in perms:
                if perm.action == action and perm.module == module:
                    return True
        return False

    @staticmethod
    def permission_required(action: Action, module: AppModule):
        async def dependency(user: User = Depends(jwt.get_current_user)):
            if not await AuthPermissionService.has_permission(user, action, module):
                raise error.forbidden()
            return user
        return dependency

