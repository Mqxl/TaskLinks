from datetime import timedelta

from fastapi import FastAPI
from argon2 import PasswordHasher
from argon2 import exceptions

import models
from auth import AuthHandler
from payloads.loginpayload import AuthDetails
from provider.basestmt import user_select_stmt

app = FastAPI()
ph = PasswordHasher()
auth_handler = AuthHandler()

@app.post('/login/')
async def login(
    auth_details: AuthDetails
):

    users = await user_select_stmt(models.Users, auth_details.username)
    try:
        ph.verify(users.password, password=auth_details.password)
        token = auth_handler.encode_token(users.name)
        return {'token': token}
    except exceptions.VerifyMismatchError:
        return {"message": "Enter correct password or username"}

@app.post('/users/list')
async def users_list(
    current_user: User = Depends(get_current_active_user)
)

