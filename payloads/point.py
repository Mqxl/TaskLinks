from typing import List

from pydantic import BaseModel


class Point(BaseModel):
    id: int
    name: str
    childs: list = []
    longitude: float
    latitude: float


class PointList(BaseModel):
    items: List[Point] = []