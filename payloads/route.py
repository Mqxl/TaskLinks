from typing import List

from pydantic import BaseModel


class Route(BaseModel):
    id: int
    name: str
    user_id: int
    points: list = []
    duration: str


class RouteList(BaseModel):
    items: List[Route] = []
