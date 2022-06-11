from typing import List, Tuple

from payloads.route import Route, RouteList
import models


async def make_point(
    record: models.Routes
):
    point = Route(
        id=record.id,
        name=record.name,
        points=record.points,
    )
    return point


async def make_point_list(
    records: List[Tuple[models.Routes]]
):
    route_list = RouteList()
    for record in records:
        route_list.items.append(
            await make_point(*record)
        )
    return route_list