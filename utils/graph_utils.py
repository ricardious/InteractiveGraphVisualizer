def get_adjacency_list(graph):
    """Convierte el grafo en una lista de adyacencia."""
    adj_list = {}
    for node in graph.nodes():
        adj_list[node] = list(graph.neighbors(node))
    return adj_list
