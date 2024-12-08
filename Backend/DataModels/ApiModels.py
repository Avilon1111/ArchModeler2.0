from pydantic import BaseModel
from typing import List, Optional
from DataModels.Statuses import *

class Model(BaseModel):
    id: str
    name: str
    author: str
    info: str

class Element(BaseModel):
    id: Optional[str] = ""
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
    visibility: Optional[Visibility] = Visibility.invisible


class Connection(Element):
    from_element: str
    to_element: str


class Arrow(Connection):
    pass


class Nest(Connection):
    pass


class ModelElements(BaseModel):
    blocks: Optional[List[Block]] = []
    arrows: Optional[List[Arrow]] = []
