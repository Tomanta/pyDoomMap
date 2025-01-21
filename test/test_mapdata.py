from wad.mapdata import Vertex


def test_vertex_creation():
    v = Vertex(0, 0)
    assert v.x == 0
    assert v.y == 0
