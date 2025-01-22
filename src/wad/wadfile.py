from typing import Final
import struct
from dataclasses import dataclass


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


class WadReader:
    def __init__(self, wadfile: str):
        self._filename: str = wadfile
        self._header: WadHeader = None
        self._waddata: bytes = None

        self._load_wad_data()
        self._read_header()

    def _load_wad_data(self):
        with open(self._filename, 'rb') as wad_file:
            self._waddata = wad_file.read()

    def _read_header(self):
        wad_type, num_lumps, directory_offset = struct.unpack_from(WAD_HEADER_LAYOUT, self._waddata,0)
        self._header = WadHeader(wad_type.decode('ascii'), num_lumps, directory_offset)