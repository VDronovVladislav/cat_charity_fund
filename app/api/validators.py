from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession
) -> None:
    charityproject_id = (
        charity_project_crud.get_charityproject_id_by_name(
            charity_project_name, session
        )
    )
    if charityproject_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Такой благотворительный проект уже создан!'
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Благотворительный проект не найден!'
        )
    return charity_project


async def check_charity_project_is_not_empty(
        charity_project_id: int,
        session: AsyncSession,
) -> None:
    invested_amount = await session.execute(
        select(CharityProject.invested_amount).where(
            CharityProject.id == charity_project_id
        )
    )
    if invested_amount != 0:
        raise HTTPException(
            status_code=422,
            detail='Нельзя удалить проект, в который уже инвестированы деньги!'
        )


async def check_charity_project_not_closed(
        charity_project_id: int,
        session: AsyncSession,
) -> None:
    fully_invested = await session.execute(
        select(CharityProject.fully_invested).where(
            CharityProject.id == charity_project_id
        )
    )
    if fully_invested is True:
        raise HTTPException(
            status_code=422,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_full_amount_not_less_than_invested(
        charity_project_id: int,
        session: AsyncSession,
) -> None:
    full_amount = await session.execute(
        select(CharityProject.full_amount).where(
            CharityProject.id == charity_project_id
        )
    )
    invested_amount = await session.execute(
        select(CharityProject.invested_amount).where(
            CharityProject.id == charity_project_id
        )
    )
    if full_amount < invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!'
        )