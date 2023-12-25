from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession
) -> None:
    charityproject_id = (
        await charity_project_crud.get_charityproject_id_by_name(
            charity_project_name, session
        )
    )
    if charityproject_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
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
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project


async def check_charity_project_not_closed(
        charity_project_id: int,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    return charity_project


async def check_full_amount_not_less_than_invested(
        charity_project: CharityProject,
        new_full_amount: int,
) -> None:
    if new_full_amount:
        if new_full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=400,
                detail='Нельзя установить требуемую сумму меньше уже вложенной!'
            )
    return charity_project