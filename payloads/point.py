from typing import List

from pydantic import BaseModel


class Point(BaseModel):
    id: int
    name: str
    childs: list = []


class PointList(BaseModel):
    items: List[Point] = []