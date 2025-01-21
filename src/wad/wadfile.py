from dataclasses import dataclass


@dataclass
class WadHeader:
    filetype: str
    numlumps: int
    directory_offset: int
