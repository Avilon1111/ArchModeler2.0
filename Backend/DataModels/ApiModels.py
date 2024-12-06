from pydantic import BaseModel
from typing import List, Optional, Union
from enum import Enum

class AbstractionLevels(str, Enum):
    Context = "Context"
    Container = "Container"
    Component = "Component"
    Code = "Code"


class Model(BaseModel):
    model_id: str
    name: str
    author: str
    info: str


class Element(BaseModel):
    id: Optional[str]
    name: str
    info: str


class HitBox(BaseModel):
    """
    coordinates of left_upper corner
    """
    width: float
    height: float
    x_axis: float
    y_axis: float
    rotation: float


class Block(Element):
    hit_box: HitBox
    type: AbstractionLevels
    visibility: bool


class Connection(Element):
    from_element: str
    to_element: str


class Arrow(Connection):
    visibility: bool


class Nest(Connection):
    pass


class ModelElements(BaseModel):
    elements: List[Block]
    arrows: List[Arrow]
