from typing import Type

import models
from alembic.devsettings import session
from sqlalchemy import select, insert, and_, Integer, cast, func
from .adapter import *
from models import Base


async def user_get_stmt(
    model: Type[Base],
    username: str,
):
    stmt = select(
        model
    ).where(
        model.name == username
    )
    record = (await session.execute(stmt)).one()

    return await make_user(*record)


async def point_select_stmt(
    model: Type[Base]
):
    stmt = select(model)
    records = (await session.execute(stmt)).all()
    return await make_point_list(records)


async def routes_select_stmt(
    model: Type[Base]
):
    stmt = select(model)
    records = (await session.execute(stmt)).all()
    return await make_point_list(records)


async def routes_insert_stmt(
    model: Type[Base],
    from_point: str,
    to_point: str,
    username: str
):
    value = {
        'name': username,
        'points': [from_point, to_point]
    }
    stmt = insert(
        model
    ).values(
        value
    ).returning(model)
    route = (await session.execute(stmt)).all()
    await session.commit()
    return route


async def get_route_recursive(
    from_point: str,
    to_point: str
):
    val = select(func.unnest(models.Points.childs))
    first_stmt = select(models.Points).where(models.Points.name == from_point).cte(recursive=True)
    second_stmt = select(models.Points).where(
        and_(
            cast(val, Integer) == models.Points.id,
            models.Points.name == to_point
        )
    )
    stmt = select(first_stmt.union_all(second_stmt))
    route = (await session.execute(stmt)).all()
    return route



