from dataclasses import dataclass
from enum import IntFlag

# ZDDoom source for automap: https://github.com/ZDoom/gzdoom/blob/master/src/am_map.cpp


class LdFlags(IntFlag):
    ML_BLOCKING = 1
    ML_BLOCKMONSTERS = 2
    ML_TWOSIDED = 4
    ML_DONTPEGSTOP = 8
    ML_DONTPEGBOTTOM = 16
    ML_SECRET = 32
    ML_SOUNDBLOCK = 64
    ML_DONTDRAW = 128
    ML_MAPPED = 256


@dataclass
class Thing:
    x_pos: int
    y_pos: int
    angle: int
    type: int
    flags: int


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


@dataclass
class Sidedef:
    x_offset: int
    y_offset: int
    upper_texture: str
    lower_texture: str
    middle_texture: str
    sector_number: int


@dataclass
class Sector:
    fl_height: int
    cl_height: int
    fl_texture: str
    cl_texture: str
    light_level: int
    special_type: int
    tag_number: int


class Map:
    def __init__(
        self,
        name: str,
        vertexes: list,
        linedefs: list,
        sidedefs: list,
        sectors: list,
        things: list,
    ):
        self.name = name
        self.vertexes = vertexes
        self.linedefs = linedefs
        self.sidedefs = sidedefs
        self.sectors = sectors
        self.things = things

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

            # if linedef.flags & LdFlags.ML_DONTDRAW:
            #    type = "hidden"
            if linedef.front_sidedef == -1 or linedef.back_sidedef == -1:
                type = "one-sided"
            elif (
                self.sectors[
                    self.sidedefs[linedef.front_sidedef].sector_number
                ].fl_height
                != self.sectors[
                    self.sidedefs[linedef.back_sidedef].sector_number
                ].fl_height
            ):
                type = "floor-diff"
            elif (
                self.sectors[
                    self.sidedefs[linedef.front_sidedef].sector_number
                ].cl_height
                != self.sectors[
                    self.sidedefs[linedef.back_sidedef].sector_number
                ].cl_height
            ):
                type = "ceil-diff"
            elif linedef.flags & LdFlags.ML_SECRET:
                type = "one-sided"

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
