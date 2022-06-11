from typing import Type
from alembic.devsettings import session
from sqlalchemy import select, insert, func
from .adapter import *
from models import Base


async def user_get_stmt(
    username: str,
):
    stmt = select(
        models.Users
    ).where(
        models.Users.name == username
    )
    record = (await session.execute(stmt)).one()

    return await make_user(*record)


async def point_select_stmt():
    stmt = select(models.Points)
    records = (await session.execute(stmt)).all()
    return await make_point_list(records)


async def point_select_stmt_with_filter(
    ids: List[str]
):
    stmt = select(models.Points).where(func.lower(models.Points.name).in_([i.lower() for i in ids]))
    records = (await session.execute(stmt)).all()
    return await make_point_list(records)


async def get_point_stmt(
    name: str
):
    stmt = select(models.Points).where(func.lower(models.Points.name) == name.lower())
    record = (await session.execute(stmt)).one()
    return await make_point(*record)


async def routes_select_stmt():
    stmt = select(models.Routes)
    records = (await session.execute(stmt)).all()
    return await make_route_list(records)


async def routes_insert_stmt(
    route: List[str],
    route_name: str,
    user_id: int,
    duration: str
):
    value = {
        'name': route_name,
        'user_id': user_id,
        'duration': duration,
        'points': route
    }
    stmt = insert(
        models.Routes
    ).values(
        value
    ).returning(models.Routes)
    route = (await session.execute(stmt)).all()
    await session.commit()
    return route


async def point_select_by_ids(
    model: Type[Base],
    ids: List[int]
):
    stmt = select(model).where(model.id.in_(ids))
    records = (await session.execute(stmt)).all()
    return await make_point_list(records)




