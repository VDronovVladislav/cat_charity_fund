from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charityproject_id_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_charityproject_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        db_charityproject_id = db_charityproject_id.scalars().first()
        return db_charityproject_id

    async def get_project_to_donate(
            self,
            session: AsyncSession
    ) -> CharityProject:
        project_to_donate = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == 0
            ).order_by(
                CharityProject.create_date
            ).limit(1)
        )
        project_to_donate = project_to_donate.scalars().first()
        return project_to_donate


charity_project_crud = CRUDCharityProject(CharityProject)