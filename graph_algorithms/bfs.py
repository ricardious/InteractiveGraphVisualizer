from collections import deque


def bfs(graph, start):
    visited = []
    queue = deque([start])
    visited_order = []

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.append(vertex)
            visited_order.append(vertex)
            queue.extend(sorted(n for n in graph[vertex] if n not in visited))

    return visited_order
