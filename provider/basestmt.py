from alembic.devsettings import session
from sqlalchemy import select
from .adapter import *


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





