from enum import Enum

class AbstractionLevels(str, Enum):
    Context = "Context"
    Container = "Container"
    Component = "Component"
    Code = "Code"

class Visibility(str, Enum):
    visible = "visible"
    invisible = "invisible"