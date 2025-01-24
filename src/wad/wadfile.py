from typing import Final
import struct
from dataclasses import dataclass
from .mapdata import Vertex, Linedef, Map

# All layouts are read in little endian
WAD_HEADER_LAYOUT: Final[str] = "<4s i i"  # 4 character string and two signed ints
DIRECTORY_LAYOUT: Final[str] = "<i i 8s"  # 2 ints and an 8 character string
VERTEX_LAYOUT: Final[str] = "<h h"  # two signed short ints
LINEDEF_LAYOUT: Final[str] = "<h h h h h h h"  # 8 signed short ints


@dataclass
class WadHeader:
    filetype: str
    numlumps: int
    directory_offset: int


@dataclass
class DirectoryEntry:
    filepos: int
    size: int
    name: str
    type: str = "Unknown"  # TODO: Good chance to play with Enums?


class WadReader:
    def __init__(self, wadfile: str):
        self._filename: str = wadfile
        self._header: WadHeader = None
        self._waddata: bytes = None
        self._directory: list[str, DirectoryEntry] = []
        self.maps = {}

        self._load_wad_data()
        self._read_header()
        self._read_directory()
        self._load_maps()

    def _load_wad_data(self):
        with open(self._filename, "rb") as wad_file:
            self._waddata = wad_file.read()

    def _read_header(self):
        wad_type, num_lumps, directory_offset = struct.unpack_from(
            WAD_HEADER_LAYOUT, self._waddata, 0
        )
        self._header = WadHeader(wad_type.decode("ascii"), num_lumps, directory_offset)

    def _load_maps(self):
        reading_map = False
        current_map = None
        for lump in self._directory:
            match lump.type:
                case "map":
                    if reading_map:
                        new_map = Map(
                            current_map["name"],
                            current_map["vertexes"],
                            current_map["linedefs"],
                        )
                        self.maps[current_map["name"]] = new_map
                        current_map = {
                            "name": lump.name,
                            "vertexes": [],
                            "linedefs": [],
                        }
                    else:
                        current_map = {
                            "name": lump.name,
                            "vertexes": [],
                            "linedefs": [],
                        }
                        reading_map = True
                case "map-vertex":
                    current_map["vertexes"] = self.read_vertex(lump)
                case "map-linedef":
                    current_map["linedefs"] = self.read_linedef(lump)
                case "map-thing":
                    pass
                case "map-sidedef":
                    pass
                case _:
                    if reading_map:
                        new_map = Map(
                            current_map["name"],
                            current_map["vertexes"],
                            current_map["linedefs"],
                        )
                        self.maps[current_map["name"]] = new_map
                        reading_map = False

    def read_vertex(self, lump):
        vertexes = []
        for i in range(0, lump.size // 4):
            x, y = struct.unpack_from(
                VERTEX_LAYOUT, self._waddata, lump.filepos + (i * 4)
            )
            vertexes.append(Vertex(x, y))

        return vertexes

    def read_linedef(self, lump):
        linedefs = []
        for i in range(0, lump.size // 14):
            (
                start_vertex,
                end_vertex,
                flags,
                special,
                tag,
                front_sidedef,
                back_sidedef,
            ) = struct.unpack_from(
                LINEDEF_LAYOUT, self._waddata, lump.filepos + (i * 14)
            )
            linedefs.append(
                Linedef(
                    start_vertex,
                    end_vertex,
                    flags,
                    special,
                    tag,
                    front_sidedef,
                    back_sidedef,
                )
            )

        return linedefs

    def _read_directory(self):
        for i in range(0, self._header.numlumps):
            filepos, size, name = struct.unpack_from(
                DIRECTORY_LAYOUT,
                self._waddata,
                self._header.directory_offset + (i * 16),
            )
            name = name.decode("ascii").strip(
                "\x00"
            )  # Convert name and strip trailing NULL characters

            match name:
                case "VERTEXES":
                    type = "map-vertex"
                case "LINEDEFS":
                    type = "map-linedef"
                case "SIDEDEFS":
                    type = "map-sidedef"
                case "THINGS":
                    type = "map-thing"
                case _:
                    if len(name) > 3 and name[3] == "MAP":
                        type = "map"
                    elif len(name) > 2 and name[0] == "E" and name[2] == "M":
                        type = "map"
                    else:
                        type = "unknown"

            entry = DirectoryEntry(filepos, size, name, type)
            self._directory.append(entry)
