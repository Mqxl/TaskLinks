from typing import List

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
    get_point_stmt,
    point_select_by_ids,
    point_select_stmt_with_filter
)
from provider.adapter.point import make_unsorted_point_list


app = FastAPI()
ph = PasswordHasher()
auth_handler = AuthHandler()


async def search_route(
    from_point: str = ...,
    to_point: str = ...,
):
    points = await point_select_stmt()
    from_point = await get_point_stmt(from_point)
    to_point = await get_point_stmt(to_point)
    adjacent = {}
    for i in range(len(points.items)):
        adjacent[str(points.items[i].id)] = points.items[i].childs

    def bfs(graph_to_search, start, end):
        queue = [[start]]
        visited = set()

        while queue:
            path = queue.pop(0)

            vertex = path[-1]

            if vertex == end:
                return path
            elif vertex not in visited:
                for current_neighbour in graph_to_search.get(vertex, []):
                    new_path = list(path)
                    new_path.append(current_neighbour)
                    queue.append(new_path)

                visited.add(vertex)
    return bfs(adjacent, str(from_point.id), str(to_point.id))


async def multy_search_route(
    points: List[str] = ...,
):
    points = await point_select_stmt_with_filter(points)
    adjacent = {}
    for i in range(len(points.items)):
        adjacent[str(points.items[i].id)] = points.items[i].childs

    def bfs(graph_to_search, start, end):
        queue = [[start]]
        visited = set()

        while queue:
            path = queue.pop(0)

            vertex = path[-1]

            if vertex == end:
                return path
            elif vertex not in visited:
                for current_neighbour in graph_to_search.get(vertex, []):
                    new_path = list(path)
                    new_path.append(current_neighbour)
                    queue.append(new_path)

                visited.add(vertex)
    path = []
    count = 0
    while count < len(points.items):
        try:
            path.append(bfs(adjacent, str(points.items[count + 1].id), str(points.items[count + 2].id)))
            count += 1
        except:
            break
    new_path = []
    if None in path:
        return None
    for i in path:
        for b in i:
            if b not in new_path:
                new_path.append(b)
    return new_path


@app.post('/login/')
async def login(
    auth_details: AuthDetails
):
    users = await user_get_stmt(auth_details.username)
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
    return await point_select_stmt()


@app.post('/user_route/list')
async def routes_list(
    username=Depends(auth_handler.auth_wrapper)
):
    return await routes_select_stmt()


@app.post('/route/only_view')
async def view_route(
    from_point: str,
    to_point: str,
    username=Depends(auth_handler.auth_wrapper)
):
    route = await get_route(from_point, to_point, username)
    return route


@app.post('/route/view_and_create')
async def create_route(
    from_point: str,
    to_point: str,
    route_name: str,
    username=Depends(auth_handler.auth_wrapper)
):
    route = await get_route(from_point, to_point, username, route_name)
    return route


@app.post('/route/multiple_create')
async def multy_create_route(
    points: List[str],
    route_name: str,
    username=Depends(auth_handler.auth_wrapper)
):
    user = await user_get_stmt(username)
    best_route = await multy_search_route(points)
    if best_route is None:
        return "You cant reach it"
    route = await point_select_by_ids(models.Points, [int(i) for i in best_route])
    if route_name is not ...:
        route_insert = await routes_insert_stmt([i.name for i in route.items], route_name, user.id, str(len(route.items)) + ' hours')
    return route


async def get_route(
    from_point: str,
    to_point: str,
    username: str,
    route_name: str = ...,
):
    user = await user_get_stmt(username)
    best_route = await search_route(from_point, to_point)
    route = await point_select_by_ids(models.Points, [int(i) for i in best_route])
    unord = []
    for i in best_route:
        for b in route.items:
            if int(i) == b.id:
                unord.append(b)
    unord = await make_unsorted_point_list(unord)
    if route_name is not ...:
        route_insert = await routes_insert_stmt([i.name for i in unord.items], route_name, user.id, str(len(route.items)) + ' hours')
    return unord

