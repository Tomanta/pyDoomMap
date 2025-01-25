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


@dataclass
class Line:
    start_vertex: tuple[int, int]
    end_vertex: tuple[int, int]
    type: str


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

    def get_lines(self, use_offsets: bool = True, padding: int = 0) -> list[Line]:
        if use_offsets:
            offset_x, offset_y = self.get_offsets()
        else:
            offset_x = 0
            offset_y = 0

        type = "standard"
        lines = []

        for linedef in self.linedefs:
            start = self.vertexes[linedef.start_vertex]
            end = self.vertexes[linedef.end_vertex]
            lines.append(
                Line(
                    start_vertex=(
                        start.x + offset_x + padding,
                        start.y + offset_y + padding,
                    ),
                    end_vertex=(end.x + offset_x + padding, end.y + offset_y + padding),
                    type=type,
                )
            )
        return lines

    def get_limits(self):
        """Get the extreme edges of the map"""
        offset_x, offset_y = self.get_offsets()
        max_x = float("-inf")
        max_y = float("-inf")
        for v in self.vertexes:
            if v.x > max_x:
                max_x = v.x
            if v.y > max_y:
                max_y = v.y
        return (max_x + offset_x, max_y + offset_y)
