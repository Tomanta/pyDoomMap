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
