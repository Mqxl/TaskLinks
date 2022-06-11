from fastapi import FastAPI, Depends
from argon2 import PasswordHasher
from argon2 import exceptions
import models
from auth import AuthHandler
from payloads.loginpayload import AuthDetails
from provider.basestmt import (
    user_get_stmt,
    point_select_stmt,
    routes_select_stmt,
    routes_insert_stmt,
    get_route_recursive
)


app = FastAPI()
ph = PasswordHasher()
auth_handler = AuthHandler()


async def search_route(
    from_point: str = ...,
    to_point: str = ...,
):
    rout = await get_route_recursive(from_point, to_point)
    return rout

@app.post('/login/')
async def login(
    auth_details: AuthDetails
):
    users = await user_get_stmt(models.Users, auth_details.username)
    try:
        ph.verify(users.password, password=auth_details.password)
        token = auth_handler.encode_token(users.name)
        return {'token': token}
    except exceptions.VerifyMismatchError:
        return {"message": "Enter correct password or username"}


@app.post('/points/list')
async def points_list(
    username=Depends(auth_handler.auth_wrapper)
):
    return await point_select_stmt(models.Points)


@app.post('/route/list')
async def routes_list(
    username=Depends(auth_handler.auth_wrapper)
):
    return await routes_select_stmt(models.Routes)


@app.post('/route/create', status_code=201)
async def create_route(
    from_point: str = ...,
    to_point: str = ...,
    username=Depends(auth_handler.auth_wrapper)
):
    best_route = await search_route(from_point, to_point)
    return best_route
    route = await routes_insert_stmt(models.Routes, from_point, to_point, username)
    return route

