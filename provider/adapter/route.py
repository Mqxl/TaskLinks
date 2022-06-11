from typing import List, Tuple

from payloads.point import Point, PointList
import models


async def make_point(
    record: models.Points
):
    point = Point(
        id=record.id,
        name=record.name,
        childs=record.childs,
    )
    return point


async def make_point_list(
    records: List[Tuple[models.Points]]
):
    point_list = PointList()
    for record in records:
        point_list.items.append(
            await make_point(*record)
        )
    return point_list