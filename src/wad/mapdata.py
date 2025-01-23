from dataclasses import dataclass


@dataclass
class Vertex:
    x: int
    y: int


@dataclass
class Linedef:
    start_vertex: int
    end_vertex: int
    flags: int
    special: int
    tag: int
    front_sidedef: int
    back_sidedef: int

class Map():
    def __init__(self, name: str, vertexes: list, linedefs: list):
        self.name = name
        self.vertexes = vertexes
        self.linedefs = linedefs
