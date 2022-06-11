from typing import List

from pydantic import BaseModel


class Route(BaseModel):
    id: int
    name: str
    points: list = []


class RouteList(BaseModel):
    items: List[Route] = []
