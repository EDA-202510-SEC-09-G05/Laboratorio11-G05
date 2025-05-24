from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as ver
from DataStructures.Graph import edge as edg


def new_graph (order, directed=False):
    """
    Initializes a new graph.
    order_capacity: Initial expected number of vertices for map sizing.
    directed: Boolean, True if graph is directed, False otherwise.
    """
    graph = {
        "directed": directed,
        "order": 0, 
        "num_edges": 0,
        "vertices": None,        
        "adjacency_list": None    
    }
   
    graph["vertices"] = map.new_map(order, 0.5)
    graph["adjacency_list"] = map.new_map(order, 0.5)
    
    return graph


def insert_vertex (my_graph, key_u, info_u):
    """
    Inserts a new vertex into the graph.
    key_u: The unique key for the vertex.
    info_u: The information/value associated with the vertex.
    """
    # Check if vertex already exists. If it does, map.put will update its value.
    # If you want to prevent overwriting, add a check here:
    # if map.get(my_graph['vertices'], key_u) is not None:
    #     raise ValueError(f"Vertex with key {key_u} already exists.")

    # Store the vertex's info in the 'vertices' map
    # Remember map.put returns the potentially new map object, so reassign
    my_graph['vertices'] = map.put(my_graph['vertices'], key_u, info_u)

    # Initialize an empty adjacency map for this new vertex
    # This map will store its outgoing edges (neighbor_key -> edge_object)
    # Using 1 as initial capacity for the inner map, load factor 0.5
    empty_adj_map = map.new_map(1, 0.5)
    my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, empty_adj_map)

    # Increment the actual count of vertices in the graph
    my_graph['order'] += 1

    return my_graph


def update_vertex_info (my_graph, key_u, new_info_u):
    """
    Updates the information associated with an existing vertex.
    key_u: The key of the vertex to update.
    new_info_u: The new information to associate with the vertex.
    """
    # Use map.get to check for vertex existence
    if map.get(my_graph['vertices'], key_u) is None:
        return None # Vertex not found, cannot update
    else:
        # Use map.put to update the value. It handles existing keys.
        my_graph['vertices'] = map.put(my_graph['vertices'], key_u, new_info_u)
    return my_graph


def add_edge (my_graph, key_u, key_v, weight):
    """
    Adds an edge from vertex key_u to vertex key_v with a given weight.
    key_u: Key of the source vertex.
    key_v: Key of the destination vertex.
    weight: Weight of the edge.
    """
    # Check if both vertices exist using map.get (efficient and correct)
    if map.get(my_graph['vertices'], key_u) is None:
        raise Exception(f"El vertice {key_u} (source) no existe.")
    if map.get(my_graph['vertices'], key_v) is None:
        raise Exception(f"El vertice {key_v} (destination) no existe.")

    # Get the adjacency map for vertex u
    # This will be a 'map' object (from map_linear_probing)
    adj_map_for_u = map.get(my_graph['adjacency_list'], key_u)

    # This should ideally not be None if insert_vertex correctly initializes it.
    # However, if it could be None, you'd initialize it here:
    if adj_map_for_u is None:
        adj_map_for_u = map.new_map(1, 0.5) # Create if missing (shouldn't be)
        my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, adj_map_for_u)

    # Create the edge object. Assuming edg.new_edge takes target key and weight.
    new_edge = edg.new_edge(key_v, weight)

    # Add the edge to the adjacency map of u
    # map.put returns the updated map object, so reassign
    updated_adj_map_for_u = map.put(adj_map_for_u, key_v, new_edge)

    # Update the main graph's adjacency list with the potentially new/updated map for key_u
    my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, updated_adj_map_for_u)

    # If the graph is undirected, add a reverse edge
    if not my_graph['directed']:
        # Get the adjacency map for vertex v
        adj_map_for_v = map.get(my_graph['adjacency_list'], key_v)
        if adj_map_for_v is None:
            adj_map_for_v = map.new_map(1, 0.5)
            my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_v, adj_map_for_v)
        
        # Create a reverse edge (v -> u) with the same weight
        reverse_edge = edg.new_edge(key_u, weight)
        updated_adj_map_for_v = map.put(adj_map_for_v, key_u, reverse_edge)
        my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_v, updated_adj_map_for_v)
        
        # For undirected graphs, an edge (u,v) counts as 1 edge, not 2.
        # So we only increment num_edges once here.
        my_graph['num_edges'] += 1
    else:
        # For directed graphs, each add_edge is one directed edge.
        my_graph['num_edges'] += 1
    
    return my_graph


def order(my_graph):
    """
    Returns the current number of vertices in the graph.
    """
    return my_graph['order'] # Now uses the correct count


def size(my_graph):
    """
    Returns the current number of edges in the graph.
    """
    return my_graph['num_edges']


def vertices(my_graph):
    """
    Returns an array_list containing the keys of all vertices in the graph.
    Leverages the map's key_set function for efficiency and encapsulation.
    """
    return map.key_set(my_graph['vertices'])


def out_degree(my_graph, key_u): # Renamed from degree_verdadera for clarity
    """
    Returns the out-degree of a given vertex (number of outgoing edges).
    """
    adj_map_for_u = map.get(my_graph['adjacency_list'], key_u)
    if adj_map_for_u is None:
        # If vertex doesn't exist or has no outgoing edges, out-degree is 0.
        # Consider raising an error if the vertex key is expected to exist.
        return 0
    return map.size(adj_map_for_u) # Use map.size for the inner adjacency map

def degree(my_graph,key_u):
    lista_adyacencia_u = map.get(my_graph['vertices'],key_u)
    if lista_adyacencia_u == None:
        raise Exception("El vertice no existe")
    numero = lista_adyacencia_u['adjacents']['size']     
    return numero


# Removed the old 'degree' function as it seemed incorrect or redundant.
# If you need in-degree, you would need to iterate through all adjacency lists
# or maintain separate reverse adjacency lists for efficiency.

# Removed get_vertex function as it exposed internal MapEntry structure.
# get_vertex_info is the proper way to retrieve vertex data.

def get_vertex_info(my_graph, key_u):
    """
    Returns the information (value) associated with a vertex.
    Returns None if the vertex with key_u does not exist.
    """
    # Do not raise an exception here; let the caller handle the None case.
    # This is useful for checks like 'if get_vertex_info(...) is None'.
    return map.get(my_graph['vertices'], key_u)


def get_adjacents(my_graph, vertex_key):
    """
    Returns the adjacency list (a map) for a given vertex.
    This map contains the outgoing edges (neighbor_key -> edge_object).
    Returns None if the vertex_key does not exist.
    """
    # This function returns the internal map itself.
    # If the vertex has no outgoing edges, it will return an empty map.
    # If the vertex_key itself doesn't exist, it will return None.
    return map.get(my_graph['adjacency_list'], vertex_key)


def adjacents(my_graph, vertex_key):
    """
    Returns an array_list of the *keys* of the vertices adjacent to vertex_key.
    This is suitable for graph traversal algorithms like DFS/BFS.
    """
    adj_map = map.get(my_graph['adjacency_list'], vertex_key)
    if adj_map is None:
        # If the vertex key doesn't exist or has no outgoing edges, return an empty array_list.
        return lt.new_list()
    
    # adj_map is a map_linear_probing, so get its keys (which are the adjacent vertex keys)
    return map.key_set(adj_map)

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

