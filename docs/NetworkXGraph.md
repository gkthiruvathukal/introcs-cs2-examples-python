# NetworkX Graph

## Type of Data Structure

A NetworkX graph is a **dynamic, library-backed graph** data structure. This repository uses `networkx.Graph`, which represents an undirected graph.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Add vertex | `add_vertex(vertex)` | Add a node to the graph | `O(1)` average |
| Add edge | `add_edge(vertex1, vertex2)` | Add an undirected edge | `O(1)` average |
| Display | `display()` | Return the adjacency mapping | `O(V + E)` |
| Shortest path | `shortest_path(start, end)` | Return an unweighted shortest path | `O(V + E)` |
| Connected components | `connected_components()` | Return all connected components | `O(V + E)` |

Actual performance depends on NetworkX internals and graph size. NetworkX emphasizes usability and algorithm coverage over maximum low-level performance.

## Implementation

In this repository, `NetworkXGraphDemo` wraps `networkx.Graph`. The methods delegate to NetworkX for node insertion, edge insertion, shortest path, connected components, and adjacency access.

This is the more realistic software engineering approach: use a mature graph library when the goal is choosing and applying graph algorithms rather than maintaining custom graph internals.

For library documentation, see [NetworkX](https://networkx.org/documentation/stable/).

## When to Use It

Use NetworkX when you need graph algorithms without implementing them yourself.

Common examples include:

- shortest paths
- connected components
- centrality measures
- graph transformations
- quick graph modeling and analysis

## When Not to Use It

Do not use NetworkX when:

- graph data is extremely large
- strict memory efficiency is required
- production latency is very tight
- you need a specialized graph database or distributed graph engine

For teaching graph internals, use the custom `Graph` demo. For large-scale production graph analytics, consider specialized systems.

## Testing Strategy

The NetworkX graph tests are in `tests/test_networkx_graph_demo.py`. They verify that the wrapper delegates correctly to NetworkX for adjacency, shortest path, and connected components.

| Behavior Checked | Test Method |
|---|---|
| Display returns the expected adjacency mapping | `test_display` |
| Shortest path returns the expected route | `test_shortest_path` |
| Connected components returns the expected component set | `test_connected_components` |
