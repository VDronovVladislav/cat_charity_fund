from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession
    ) -> list[Donation]:
        user_donations = await session.execute(
            select(Donation).where(
                user.id == Donation.user_id
            )
        )
        user_donations = user_donations.scalars().all()
        return user_donations

    async def get_donation_for_project(
            self,
            session: AsyncSession
    ) -> Donation:
        donation_to_donate = await session.execute(
            select(Donation).where(
                Donation.fully_invested != 1
            ).order_by(
                Donation.create_date
            ).limit(1)
        )
        donation_to_donate = donation_to_donate.scalars().first()
        return donation_to_donate


donation_crud = CRUDDonation(Donation)