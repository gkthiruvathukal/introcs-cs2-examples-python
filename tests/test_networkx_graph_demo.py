import pytest

from data_structures.networkx_graph_demo import NetworkXGraphDemo


VERTICES = ["A", "B", "C", "D"]
EDGES = [("A", "B"), ("A", "C"), ("B", "D")]


@pytest.fixture
def graph():
    graph = NetworkXGraphDemo()
    for vertex in VERTICES:
        graph.add_vertex(vertex)
    for vertex1, vertex2 in EDGES:
        graph.add_edge(vertex1, vertex2)
    return graph


def test_display(graph):
    assert graph.display() == {
        "A": {"B": {}, "C": {}},
        "B": {"A": {}, "D": {}},
        "C": {"A": {}},
        "D": {"B": {}},
    }


def test_shortest_path(graph):
    assert graph.shortest_path("A", "D") == ["A", "B", "D"]


def test_connected_components(graph):
    assert graph.connected_components() == [set(VERTICES)]
