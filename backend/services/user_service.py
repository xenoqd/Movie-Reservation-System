from backend.repositories.user_repository import user_repo
from backend.core.exceptions import DomainError
from backend.models.user import UserRole

from sqlalchemy.ext.asyncio import AsyncSession


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
            raise DomainError(
                404,
                "Acting user not found"
            )

        if not target_user:
            raise DomainError(
                404,
                "Target user not found"
            )

        if current_user.role != UserRole.ADMIN:
            raise DomainError(
                403,
                "Insufficient permissions"
            )

        if target_user.role == UserRole.ADMIN:
            raise DomainError(
                404,
                "User already ADMIN"
            )

        target_user.role = UserRole.ADMIN
        session.add(target_user)
        await session.commit()
        await session.refresh(target_user)

        return target_user
