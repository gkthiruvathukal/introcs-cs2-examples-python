import pytest

from data_structures.graph_demo import Graph


VERTICES = ["A", "B", "C", "D"]
EDGES = [("A", "B"), ("A", "C"), ("B", "D")]


@pytest.fixture
def graph():
    graph = Graph()
    for vertex in VERTICES:
        graph.add_vertex(vertex)
    for vertex1, vertex2 in EDGES:
        graph.add_edge(vertex1, vertex2)
    return graph


def test_display(graph):
    assert graph.display() == {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A"],
        "D": ["B"],
    }


def test_bfs(graph):
    assert graph.bfs("A") == ["A", "B", "C", "D"]


def test_dfs(graph):
    assert graph.dfs("A") == ["A", "B", "D", "C"]


def test_dfs_iterative_matches_recursive_order(graph):
    assert graph.dfs_iterative("A") == graph.dfs("A")


def test_recursive_dfs_raises_recursion_error_for_deep_graph(
    temporary_recursion_limit,
):
    graph = Graph()
    vertices = list(range(350))
    for vertex in vertices:
        graph.add_vertex(vertex)
    for index in range(len(vertices) - 1):
        graph.add_edge(vertices[index], vertices[index + 1])

    temporary_recursion_limit(200)
    with pytest.raises(RecursionError):
        graph.dfs(vertices[0])
    assert graph.dfs_iterative(vertices[0]) == vertices
