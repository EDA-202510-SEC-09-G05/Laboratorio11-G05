from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as ver
from DataStructures.Graph import edge as edg 

def new_graph (order_capacity, directed = True):
    """
    Initializes a new directed graph.
    order_capacity: Initial expected number of vertices for map sizing.
    """
    graph = {
        "directed": True, 
        "order": 0,
        "num_edges": 0,
        "vertices": None,
        "adjacency_list": None
        
    }

    graph["vertices"] = map.new_map(order_capacity, 0.5)
    graph["adjacency_list"] = map.new_map(order_capacity, 0.5)

    return graph


def insert_vertex (my_graph, key_u, info_u):
    """
    Inserts a new vertex into the graph.
    key_u: The unique key for the vertex.
    info_u: The information/value associated with the vertex.
    """
    my_graph['vertices'] = map.put(my_graph['vertices'], key_u, info_u)

    my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, map.new_map(1, 0.5))


    my_graph['order'] += 1

    return my_graph


def update_vertex_info (my_graph, key_u, new_info_u):
    """
    Updates the information associated with an existing vertex.
    key_u: The key of the vertex to update.
    new_info_u: The new information to associate with the vertex.
    """
    if map.get(my_graph['vertices'], key_u) is None:
        return None
    else:
        my_graph['vertices'] = map.put(my_graph['vertices'], key_u, new_info_u)
    return my_graph


def add_edge (my_graph, key_u, key_v, weight):
    """
    Adds a directed edge from vertex key_u to vertex key_v with a given weight.
    key_u: Key of the source vertex.
    key_v: Key of the destination vertex.
    weight: Weight of the edge.
    """
    if map.get(my_graph['vertices'], key_u) is None:
        raise Exception(f"El vertice {key_u} (source) no existe.")
    if map.get(my_graph['vertices'], key_v) is None:
        raise Exception(f"El vertice {key_v} (destination) no existe.")

    
    adj_map_for_u = map.get(my_graph['adjacency_list'], key_u)
    if adj_map_for_u is None: 
        adj_map_for_u = map.new_map(1, 0.5)
        my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, adj_map_for_u)

    
    edge_already_exists = map.get(adj_map_for_u, key_v) is not None

    
    new_edge = edg.new_edge(key_v, weight)
    my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, map.put(adj_map_for_u, key_v, new_edge))

    
    if not edge_already_exists:
        my_graph['num_edges'] += 1

    return my_graph


def order(my_graph):
    """
    Returns the current number of vertices in the graph.
    """
    return my_graph['order']


def size(my_graph):
    """
    Returns the current number of edges in the graph.
    """
    return my_graph['num_edges']


def vertices(my_graph):
    """
    Returns an array_list containing the keys of all vertices in the graph.
    """
    return map.key_set(my_graph['vertices'])


def out_degree(my_graph, key_u):
    """
    Returns the out-degree of a given vertex (number of outgoing edges).
    """
    
    if map.get(my_graph['vertices'], key_u) is None:
        raise Exception(f"El vertice {key_u} no existe.")

    adj_map_for_u = map.get(my_graph['adjacency_list'], key_u)
    if adj_map_for_u is None:
        return 0 
    return map.size(adj_map_for_u)


def degree(my_graph,key_u):
    lista_adyacencia_u = map.get(my_graph['vertices'],key_u)
    if lista_adyacencia_u == None:
        raise Exception("El vertice no existe")
    numero = lista_adyacencia_u['adjacents']['size']     
    return numero


def get_vertex_info(my_graph, key_u):
    """
    Returns the information (value) associated with a vertex.
    Returns None if the vertex with key_u does not exist.
    """
    return map.get(my_graph['vertices'], key_u)


def get_adjacents(my_graph, vertex_key):
    """
    Returns the adjacency list (a map) for a given vertex (outgoing edges).
    This map contains the outgoing edges (neighbor_key -> edge_object).
    Returns None if the vertex_key does not exist or has no outgoing edges.
    """
    # This returns the internal map itself.
    return map.get(my_graph['adjacency_list'], vertex_key)


def adjacents(my_graph, vertex_key):
    """
    Returns an array_list of the *keys* of the vertices adjacent to vertex_key (outgoing neighbors).
    This is suitable for graph traversal algorithms like DFS/BFS.
    """
    adj_map = map.get(my_graph['adjacency_list'], vertex_key)
    if adj_map is None:
        return lt.new_list()

    return map.key_set(adj_map)


