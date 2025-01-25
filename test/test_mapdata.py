from wad.mapdata import Vertex, Linedef, Map, Thing, Line, Sidedef, Sector


def test_vertex_creation():
    v = Vertex(0, 0)
    assert v.x == 0
    assert v.y == 0


def test_linedef_creation():
    ld = Linedef(0, 1, 14, 123, 12, 1, 0)
    assert ld.start_vertex == 0
    assert ld.end_vertex == 1
    assert ld.flags == 14
    assert ld.special == 123
    assert ld.tag == 12
    assert ld.front_sidedef == 1
    assert ld.back_sidedef == 0


def test_thing_creation():
    thing = Thing(1, 2, 45, 15, 6)
    assert thing.x_pos == 1
    assert thing.y_pos == 2
    assert thing.angle == 45
    assert thing.type == 15
    assert thing.flags == 6


def test_line_creation():
    line = Line((15, 20), (7, 45), "standard")
    assert line.start_vertex == (15, 20)
    assert line.end_vertex == (7, 45)
    assert line.type == "standard"


def test_sidedef_creation():
    sidedef = Sidedef(0, 15, "UPTEXT1", "LWTEXT1", "MIDTEXT1", 20)
    assert sidedef.x_offset == 0
    assert sidedef.y_offset == 15
    assert sidedef.upper_texture == "UPTEXT1"
    assert sidedef.lower_texture == "LWTEXT1"
    assert sidedef.middle_texture == "MIDTEXT1"
    assert sidedef.sector_number == 20


def test_sector_creation():
    sector = Sector(0, 15, "FLTEXT1", "CLTEXT1", 100, 15, 6)
    assert sector.fl_height == 0
    assert sector.cl_height == 15
    assert sector.fl_texture == "FLTEXT1"
    assert sector.cl_texture == "CLTEXT1"
    assert sector.light_level == 100
    assert sector.special_type == 15
    assert sector.tag_number == 6


def test_map_creation():
    name = "E1M1"
    vertexes = [Vertex(-30, 30), Vertex(-15, 0), Vertex(30, 27), Vertex(18, 92)]
    linedefs = [Linedef(0, 1, 14, 123, 12, 1, 0)]
    sidedefs = []
    sectors = []
    things = []
    map = Map(name, vertexes, linedefs, sidedefs, sectors, things)
    assert map.name == name
    assert map.vertexes == vertexes
    assert map.linedefs == linedefs


def test_map_get_offsets():
    name = "E1M1"
    vertexes = [Vertex(-30, 30), Vertex(-15, 0), Vertex(30, 27), Vertex(18, 92)]
    linedefs = [Linedef(0, 1, 14, 123, 12, 1, 0)]
    sidedefs = []
    sectors = []
    things = []
    map = Map(name, vertexes, linedefs, sidedefs, sectors, things)
    offsets = map.get_offsets()
    assert offsets[0] == 30
    assert offsets[1] == 0
