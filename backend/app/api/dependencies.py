from fastapi import HTTPException, status


async def get_current_user_id() -> int:
    """
    Temporary development authentication dependency.

    This will be replaced by JWT authentication in Phase 2.
    """
    user_id = 1

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    return user_id