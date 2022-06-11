from payloads.user import User, UserList
import models


async def make_user(
    record: models.Users
):
    user = User(
        id=record.id,
        name=record.name,
        email=record.email,
        password=record.password
    )
    return user

