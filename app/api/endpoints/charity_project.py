from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import charity_project_crud
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjecUpdate)
from app.api.validators import (check_name_duplicate,
                                check_charity_project_exists,
                                check_charity_project_is_not_empty,
                                check_full_amount_not_less_than_invested,
                                check_charity_project_not_closed)
from app.services import create_project_and_donate
from app.core.user import current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    await charity_project_crud.create(
        charity_project, session
    )
    return await create_project_and_donate(session)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjecUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    await check_charity_project_not_closed(
        project_id, session
    )
    await check_full_amount_not_less_than_invested(
        charity_project, obj_in.full_amount
    )
    return await charity_project_crud.update(charity_project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_is_not_empty(
        project_id, session
    )
    return await charity_project_crud.remove(charity_project, session)