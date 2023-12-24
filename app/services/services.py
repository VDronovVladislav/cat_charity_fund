from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject, Donation


def calculation(donation, project_to_donate):
    donation_total = donation.full_amount
    required_amount = (
        project_to_donate.full_amount - project_to_donate.invested_amount
    )
    if donation_total >= required_amount:
        donation_total -= required_amount
        project_to_donate.invested_amount += required_amount
        project_to_donate.fully_invested = True
        project_to_donate.close_date = datetime.now()
        donation.invested_amount = required_amount
    else:
        project_to_donate.invested_amount += donation_total
        donation.invested_amount = donation_total
        donation.fully_invested = True
        donation.close_date = datetime.now()
        donation_total = 0

    return donation_total, project_to_donate, donation


async def create_donation(
        donation: Donation,
        session: AsyncSession,
) -> Donation:
    donation_total = donation.full_amount
    while donation_total != 0:
        project_to_donate = await charity_project_crud.get_project_to_donate(
            session
        )
        if project_to_donate:
            donation_total, project_to_donate, donation = calculation(donation, project_to_donate)
            session.add(donation)
            session.add(project_to_donate)
            await session.commit()
            await session.refresh(project_to_donate)
            await session.refresh(donation)
        else:
            break
    return donation


async def create_project_and_donate(
        session: AsyncSession
) -> CharityProject:
    project_to_donate = await charity_project_crud.get_project_to_donate(
        session
    )
    while project_to_donate.fully_invested is not True:
        donation_to_donate = await donation_crud.get_donation_for_project(
            session
        )
        if donation_to_donate:
            donation_total, project, donation_to_donate = calculation(donation_to_donate, project_to_donate)
            session.add(donation_to_donate)
            session.add(project_to_donate)
            await session.commit()
            await session.refresh(project_to_donate)
            await session.refresh(donation_to_donate)
        else:
            break
    return project_to_donate