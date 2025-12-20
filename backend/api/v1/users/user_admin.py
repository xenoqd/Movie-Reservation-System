from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies.auth import get_current_user
from backend.models.user import User
from backend.schemas.user import UserRead
from backend.services.user_service import UserService
from backend.db.session import get_session

user_admin_router = APIRouter(prefix="/admin", tags=["admin", "user_admin"])


@user_admin_router.post(
    "/users/{target_user_id}/promote",
    response_model=UserRead
)
async def promote_user(
    target_user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    result = await UserService.promote_user_to_admin(
        current_user.id, 
        target_user_id, 
        session
    )

    return result
