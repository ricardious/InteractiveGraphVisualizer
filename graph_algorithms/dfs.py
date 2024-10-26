def dfs(graph, start, visited=None, visited_order=None):
    if visited is None:
        visited = set()
    if visited_order is None:
        visited_order = []

    visited.add(start)
    visited_order.append(start)

    for next_vertex in sorted(graph[start]):
        if next_vertex not in visited:
            dfs(graph, next_vertex, visited, visited_order)

    return visited_order
