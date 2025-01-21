from wad.wadfile import WadHeader


def test_wad_header_creation():
    header = WadHeader("IWAD", 450, 123456)
    assert header.filetype == "IWAD"
    assert header.numlumps == 450
    assert header.directory_offset == 123456
