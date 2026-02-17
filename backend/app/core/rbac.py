from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.core.security import TokenPayload, get_current_user



def require_roles(*roles: str) -> Callable[[TokenPayload], TokenPayload]:
    def dependency(user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        if user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user.get('role')}' is not allowed",
            )
        return user

    return dependency
