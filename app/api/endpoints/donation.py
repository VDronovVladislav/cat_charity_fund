from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import donation_crud
from app.schemas import DonationDB, DonationCreate, DonationLowDB
from app.models import User
from app.services import create_donation


router = APIRouter()


@router.post(
    '/',
    response_model=DonationLowDB,
    dependencies=[Depends(current_user)],
    #response_model_exclude={'comment'}
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(
        donation, session, user
    )
    new_donation = await create_donation(new_donation, session)

    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationLowDB],
    dependencies=[Depends(current_user)]
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    user_donations = await donation_crud.get_by_user(
        user, session
    )
    return user_donations