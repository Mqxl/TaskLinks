from typing import Type

import models
from alembic.devsettings import session
from sqlalchemy import select
from payloads.user import User, UserList


async def make_users(
    record: models.Users
):
    user = User(
        name=record.name,
        email=record.email,
        password=record.password
    )
    return user


async def user_select_stmt(
    model: Type,
    username: str,
):
    stmt = select(
        model
    ).where(
        model.name == username
    )
    record = (await session.execute(stmt)).one()

    user = await make_users(*record)

    return user
