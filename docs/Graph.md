# Graph

## Type of Data Structure

A graph is a **dynamic, non-linear relationship** data structure. It stores vertices and edges; this repository's `Graph` is undirected.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Add vertex | `add_vertex(vertex)` | Add a vertex if missing | `O(1)` average |
| Add edge | `add_edge(vertex1, vertex2)` | Add an undirected edge between existing vertices | `O(1)` average |
| Display | `display()` | Return the adjacency list | `O(V + E)` |
| Breadth-first search | `bfs(start_vertex)` | Traverse by distance from start | `O(V + E)` |
| Depth-first search | `dfs(start_vertex)` | Recursive DFS traversal | `O(V + E)` |
| Iterative DFS | `dfs_iterative(start_vertex)` | DFS using an explicit stack | `O(V + E)` |

`V` is the number of vertices and `E` is the number of edges.

## Implementation

In this repository, `Graph` is implemented with an adjacency-list dictionary. Each vertex maps to a list of neighboring vertices. `add_edge(...)` appends each endpoint to the other's neighbor list, making the graph undirected.

Recursive DFS is included for clarity. `dfs_iterative(...)` shows the equivalent explicit-stack version and avoids Python recursion limits on deep graphs.

For a language-neutral overview, see [Graph (abstract data type)](https://en.wikipedia.org/wiki/Graph_(abstract_data_type)).

## When to Use It

Use a graph when relationships matter as much as the data items.

Common examples include:

- networks
- maps and routes
- prerequisite relationships
- social connections
- dependency analysis

## When Not to Use It

Do not use this simple graph when you need:

- weighted edges
- directed edges
- industrial-strength algorithms
- very large graph performance
- duplicate-edge control

For richer graph work in Python, prefer NetworkX or another graph library.

## Testing Strategy

The graph tests are in `tests/test_graph_demo.py`. They verify adjacency-list output, BFS order, recursive DFS order, iterative DFS parity, and recursion-limit behavior.

| Behavior Checked | Test Method |
|---|---|
| Display returns the expected adjacency list | `test_display` |
| BFS traverses vertices in breadth-first order | `test_bfs` |
| Recursive DFS traverses vertices in expected order | `test_dfs` |
| Iterative DFS matches recursive DFS order | `test_dfs_iterative_matches_recursive_order` |
| Recursive DFS raises `RecursionError` on a deep graph while iterative DFS succeeds | `test_recursive_dfs_raises_recursion_error_for_deep_graph` |
