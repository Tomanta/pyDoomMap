from wad.wadfile import WadHeader, WadReader
from pathlib import Path


WAD_FILENAME: str = Path('wad') / Path('DOOM1.wad')

def test_wad_header_creation():
    header = WadHeader("IWAD", 450, 123456)
    assert header.filetype == "IWAD"
    assert header.numlumps == 450
    assert header.directory_offset == 123456

def test_create_reader():
    wad_reader = WadReader(WAD_FILENAME)
    assert wad_reader._filename == WAD_FILENAME

def test_read_header():
    wad_reader = WadReader(WAD_FILENAME)
    header = WadHeader("IWAD", 1264, 4175796)
    assert wad_reader._header == header