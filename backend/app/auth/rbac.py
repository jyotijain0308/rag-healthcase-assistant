from fastapi import Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.auth.rbac_map import ROLE_PERMISSIONS

import logging
logger = logging.getLogger("audit")

def require_permissions(required_permissions: list[str]):
    def checker(user=Depends(get_current_user)):

        user_role = user["role"]
        user_permissions = ROLE_PERMISSIONS.get(user_role, [])
        logger.info(f"USER={user['user_id']} ROLE={user['role']} ACTION={required_permissions}")

        # check intersection
        allowed = any(
            perm in user_permissions
            for perm in required_permissions
        )

        print(f"{user_role} has access to {required_permissions} =>", allowed);

        if not allowed:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )
        return user
    return checker