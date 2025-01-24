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


class Map:
    def __init__(self, name: str, vertexes: list, linedefs: list):
        self.name = name
        self.vertexes = vertexes
        self.linedefs = linedefs

    def get_offsets(self):
        """Vertexes can be negative, this returns an offset that can be added to every vertex to adjust them to a 0-based grid."""
        min_x = 0
        min_y = 0
        for v in self.vertexes:
            if v.x < min_x:
                min_x = v.x
            if v.y < min_y:
                min_y = v.y

        return (abs(min_x), abs(min_y))

    def get_limits(self):
        offset_x, offset_y = self.get_offsets()
        max_x = 0
        max_y = 0
        for v in self.vertexes:
            if v.x > max_x:
                max_x = v.x
            if v.y > max_y:
                max_y = v.y
        return (max_x + offset_x, max_y + offset_y)
