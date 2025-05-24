from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as ver
from DataStructures.Graph import edge as edg # Assuming edg.new_edge(key, weight) exists

def new_graph (order_capacity): # Removed 'directed' parameter, it's always True
    """
    Initializes a new directed graph.
    order_capacity: Initial expected number of vertices for map sizing.
    """
    graph = {
        "directed": True, # Always true for this implementation
        "order": 0,
        "num_edges": 0,
        "vertices": None,
        "adjacency_list": None,
        "reverse_adjacency_list": None # Added for efficient in_degree calculation
    }

    graph["vertices"] = map.new_map(order_capacity, 0.5)
    graph["adjacency_list"] = map.new_map(order_capacity, 0.5)
    graph["reverse_adjacency_list"] = map.new_map(order_capacity, 0.5) # Initialize reverse adj list

    return graph


def insert_vertex (my_graph, key_u, info_u):
    """
    Inserts a new vertex into the graph.
    key_u: The unique key for the vertex.
    info_u: The information/value associated with the vertex.
    """
    # If vertex already exists, map.put will update its value.
    my_graph['vertices'] = map.put(my_graph['vertices'], key_u, info_u)

    # Initialize empty adjacency maps for this new vertex
    # Both for outgoing and incoming edges
    my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, map.new_map(1, 0.5))
    my_graph['reverse_adjacency_list'] = map.put(my_graph['reverse_adjacency_list'], key_u, map.new_map(1, 0.5))

    # Increment the actual count of vertices in the graph
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

    # --- Handle Outgoing Edge (key_u -> key_v) ---
    adj_map_for_u = map.get(my_graph['adjacency_list'], key_u)
    # This should never be None if insert_vertex is used correctly
    if adj_map_for_u is None:
        adj_map_for_u = map.new_map(1, 0.5)
        my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, adj_map_for_u)

    edge_already_exists = map.get(adj_map_for_u, key_v) is not None

    new_edge = edg.new_edge(key_v, weight)
    my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, map.put(adj_map_for_u, key_v, new_edge))

    # --- Handle Incoming Edge (key_v <- key_u) for reverse_adjacency_list ---
    reverse_adj_map_for_v = map.get(my_graph['reverse_adjacency_list'], key_v)
    # This should never be None if insert_vertex is used correctly
    if reverse_adj_map_for_v is None:
        reverse_adj_map_for_v = map.new_map(1, 0.5)
        my_graph['reverse_adjacency_list'] = map.put(my_graph['reverse_adjacency_list'], key_v, reverse_adj_map_for_v)

    # For the reverse list, we store the source key and edge object
    # The 'to' field in the edge object will still point to the destination from the original edge (key_v)
    # but the key in the reverse map is the source key (key_u).
    my_graph['reverse_adjacency_list'] = map.put(my_graph['reverse_adjacency_list'], key_v, map.put(reverse_adj_map_for_v, key_u, new_edge))

    # Increment num_edges ONLY if this is a truly new directed edge
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
    adj_map_for_u = map.get(my_graph['adjacency_list'], key_u)
    if adj_map_for_u is None:
        # If vertex doesn't exist or has no outgoing edges, out-degree is 0.
        # Could raise an error if key_u is not expected to be missing from vertices.
        if map.get(my_graph['vertices'], key_u) is None:
            raise Exception(f"El vertice {key_u} no existe.")
        return 0 # Vertex exists but has no outgoing edges
    return map.size(adj_map_for_u)


def in_degree(my_graph, key_u):
    """
    Returns the in-degree of a given vertex (number of incoming edges).
    """
    reverse_adj_map_for_u = map.get(my_graph['reverse_adjacency_list'], key_u)
    if reverse_adj_map_for_u is None:
        # If vertex doesn't exist or has no incoming edges, in-degree is 0.
        if map.get(my_graph['vertices'], key_u) is None:
            raise Exception(f"El vertice {key_u} no existe.")
        return 0 # Vertex exists but has no incoming edges
    return map.size(reverse_adj_map_for_u)


def out_degree(my_graph, key_u):
    """
    Returns the total degree of a given vertex (in-degree + out-degree) for a directed graph.
    """
    # Check if the vertex exists first
    if map.get(my_graph['vertices'], key_u) is None:
        raise Exception(f"El vertice {key_u} no existe.")

    return out_degree(my_graph, key_u) + in_degree(my_graph, key_u)

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
    # This returns the internal map itself. If the vertex has no outgoing edges,
    # it will return an empty map (if the key exists but map.new_map was size 1)
    # or None if the key doesn't exist.
    return map.get(my_graph['adjacency_list'], vertex_key)


def adjacents(my_graph, vertex_key):
    """
    Returns an array_list of the *keys* of the vertices adjacent to vertex_key (outgoing neighbors).
    This is suitable for graph traversal algorithms like DFS/BFS.
    """
    adj_map = map.get(my_graph['adjacency_list'], vertex_key)
    if adj_map is None:
        # If the vertex key doesn't exist or has no outgoing edges, return an empty array_list.
        return lt.new_list()

    return map.key_set(adj_map)


def predecessors(my_graph, vertex_key):
    """
    Returns an array_list of the *keys* of the vertices that have an incoming edge to vertex_key.
    """
    rev_adj_map = map.get(my_graph['reverse_adjacency_list'], vertex_key)
    if rev_adj_map is None:
        return lt.new_list()
    return map.key_set(rev_adj_map)

a = new_graph(10)
b = insert_vertex(a,'si',"AJA THATS MY SHIT")
b = insert_vertex(a,'no',"mucho texto")
b = insert_vertex(a,'Pablo',{'codigo':2023,
                             'Altura': 1.85})
b = insert_vertex(a,'martin',{'codigo':2024,
                             'Altura': 1.75})
b = insert_vertex(a,'Tomi',{'codigo':2022,
                             'Altura': 1.65})

d = add_edge(a,"si","no",3.0)
d = add_edge(a,"no","si",4.4)
d = add_edge(a,'Pablo','martin',9)
d = add_edge(a,"martin", 'Pablo',1)
d = add_edge(a,"Pablo",'Tomi', 100)

print(a)
