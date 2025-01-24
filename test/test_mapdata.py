from wad.mapdata import Vertex, Linedef, Map


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


def test_map_creation():
    name = "E1M1"
    vertexes = [Vertex(-30, 30), Vertex(-15, 0), Vertex(30, 27), Vertex(18, 92)]
    linedefs = [Linedef(0, 1, 14, 123, 12, 1, 0)]
    map = Map(name, vertexes, linedefs)
    assert map.name == name
    assert map.vertexes == vertexes
    assert map.linedefs == linedefs


def test_map_get_offsets():
    name = "E1M1"
    vertexes = [Vertex(-30, 30), Vertex(-15, 0), Vertex(30, 27), Vertex(18, 92)]
    linedefs = [Linedef(0, 1, 14, 123, 12, 1, 0)]
    map = Map(name, vertexes, linedefs)
    offsets = map.get_offsets()
    assert offsets[0] == 30
    assert offsets[1] == 0
