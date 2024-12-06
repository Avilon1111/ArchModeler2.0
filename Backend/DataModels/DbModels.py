from enum import Enum

class JSON(dict):
    pass


class CollectionNames(str, Enum):
    blocks = "blocks"
    nests = "nests"
    arrows = "arrows"


