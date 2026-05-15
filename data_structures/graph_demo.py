class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        """Add a new vertex to the graph."""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2):
        """Add an undirected edge between vertex1 and vertex2."""
        if vertex1 in self.adjacency_list and vertex2 in self.adjacency_list:
            self.adjacency_list[vertex1].append(vertex2)
            self.adjacency_list[vertex2].append(vertex1)

    def display(self):
        """Display the adjacency list of the graph."""
        return dict(self.adjacency_list)

    def bfs(self, start_vertex):
        """Perform Breadth-First Search (BFS) from the start_vertex."""
        visited = set()
        queue = [start_vertex]
        traversal = []

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                traversal.append(vertex)
                visited.add(vertex)
                queue.extend([v for v in self.adjacency_list[vertex] if v not in visited])

        return traversal

    def dfs(self, start_vertex):
        """Perform Depth-First Search (DFS) from the start_vertex."""
        visited = set()
        traversal = []

        def dfs_recursive(vertex):
            if vertex not in visited:
                traversal.append(vertex)
                visited.add(vertex)
                for neighbor in self.adjacency_list[vertex]:
                    dfs_recursive(neighbor)

        dfs_recursive(start_vertex)
        return traversal

    def dfs_iterative(self, start_vertex):
        """Perform Depth-First Search (DFS) using an explicit stack."""
        visited = set()
        stack = [start_vertex]
        traversal = []

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                traversal.append(vertex)
                visited.add(vertex)
                for neighbor in reversed(self.adjacency_list[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return traversal
