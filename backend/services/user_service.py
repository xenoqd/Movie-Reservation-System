from backend.repositories.user_repository import user_repo
from backend.models.user import UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status


class UserService:
    @staticmethod
    async def promote_user_to_admin(
        current_user: int, 
        target_user: int, 
        session: AsyncSession
    ):

        if session is None:
            raise RuntimeError("Session must be provided")

        current_user = await user_repo.get_by_user_id(session, current_user)
        target_user = await user_repo.get_by_user_id(session, target_user)

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Acting user not found"
            )

        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Target user not found"
            )

        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not enough rights"
            )

        if target_user.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="User already ADMIN"
            )

        target_user.role = UserRole.ADMIN
        session.add(target_user)
        await session.commit()
        await session.refresh(target_user)

        return target_user
