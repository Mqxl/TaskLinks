from typing import List, Tuple

from payloads.route import Route, RouteList
import models


async def make_route(
    record: models.Routes
):
    route = Route(
        id=record.id,
        name=record.name,
        user_id=record.user_id,
        points=record.points,
        duration=record.duration
    )
    return route


async def make_route_list(
    records: List[Tuple[models.Routes]]
):
    route_list = RouteList()
    for record in records:
        route_list.items.append(
            await make_route(*record)
        )
    return route_list
