# DataStructures/Graph/no_digraph.py

from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as ver
from DataStructures.Graph import edge as edg 



def new_graph (order, directed=False):
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
    my_graph['vertices'] = map.put(my_graph['vertices'], key_u, info_u)
    empty_adj_map = map.new_map(1, 0.5)
    my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, empty_adj_map)
    my_graph['order'] += 1
    return my_graph

def update_vertex_info (my_graph, key_u, new_info_u):
    if map.get(my_graph['vertices'], key_u) is None:
        return None
    else:
        my_graph['vertices'] = map.put(my_graph['vertices'], key_u, new_info_u)
    return my_graph

def add_edge (my_graph, key_u, key_v, weight):
    if map.get(my_graph['vertices'], key_u) is None:
        raise Exception(f"El vertice {key_u} (source) no existe.")
    if map.get(my_graph['vertices'], key_v) is None:
        raise Exception(f"El vertice {key_v} (destination) no existe.")

    adj_map_for_u = map.get(my_graph['adjacency_list'], key_u)
    if adj_map_for_u is None:
        adj_map_for_u = map.new_map(1, 0.5)
        my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, adj_map_for_u)

    new_edge = edg.new_edge(key_v, weight)
    updated_adj_map_for_u = map.put(adj_map_for_u, key_v, new_edge)
    my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, updated_adj_map_for_u)

    if not my_graph['directed']:
        adj_map_for_v = map.get(my_graph['adjacency_list'], key_v)
        if adj_map_for_v is None:
            adj_map_for_v = map.new_map(1, 0.5)
            my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_v, adj_map_for_v)
        
        reverse_edge = edg.new_edge(key_u, weight)
        updated_adj_map_for_v = map.put(adj_map_for_v, key_u, reverse_edge)
        my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_v, updated_adj_map_for_v)
        
        edge_exists_u_v = map.get(adj_map_for_u, key_v) is not None
        edge_exists_v_u = map.get(adj_map_for_v, key_u) is not None
        if not edge_exists_u_v and not edge_exists_v_u:
             my_graph['num_edges'] += 1
    else:
        edge_exists_u_v = map.get(adj_map_for_u, key_v) is not None
        if not edge_exists_u_v:
             my_graph['num_edges'] += 1
    
    return my_graph

def order(my_graph):
    return my_graph['order']

def size(my_graph):
    return my_graph['num_edges']

def vertices(my_graph):
    return map.key_set(my_graph['vertices'])

def out_degree(my_graph, key_u):
    if map.get(my_graph['vertices'], key_u) is None:
        raise Exception(f"El vertice {key_u} no existe.")
    adj_map_for_u = map.get(my_graph['adjacency_list'], key_u)
    if adj_map_for_u is None:
        return 0
    return map.size(adj_map_for_u)

# As per your assignment, this function remains exactly as is.
def degree(my_graph,key_u):
    lista_adyacencia_u = map.get(my_graph['vertices'],key_u)
    if lista_adyacencia_u == None:
        raise Exception("El vertice no existe")
    numero = lista_adyacencia_u['adjacents']['size']     
    return numero


def get_adjacents(my_graph, vertex_key):
    """
    Returns the adjacency list (a map) for a given vertex.
    This map contains the outgoing edges (neighbor_key -> edge_object).
    Returns None if the vertex_key does not exist.
    Returns an empty map if the vertex exists but has no outgoing edges.
    """
    # First, check if the vertex_key exists in the graph's main vertices map
    if map.get(my_graph['vertices'], vertex_key) is None:
        return None # Vertex does not exist, so no adjacency map for it

    # Get the adjacency map for this specific vertex
    adj_map = map.get(my_graph['adjacency_list'], vertex_key)
    
    # If the adjacency map hasn't been initialized yet for this vertex (unlikely with insert_vertex)
    if adj_map is None:
        # It's an existing vertex with no edges yet. Return an empty map.
        return map.new_map(1, 0.5) # <--- FIX: Returns a proper map, not an array_list
    
    return adj_map # <--- FIX: Returns the actual map object, not its keys

# This function should return an array_list of keys, and is called by DFS/BFS.
# Its name 'adjacents' implies it returns 'what is adjacent'.
def adjacents(my_graph, vertex_key):
    """
    Returns an array_list containing the *keys* of the vertices adjacent to vertex_key.
    This is suitable for graph traversal algorithms like DFS/BFS.
    """
    # First, get the actual adjacency map using the corrected get_adjacents.
    # This might return None (if vertex doesn't exist) or an empty map (if no edges).
    adj_map = get_adjacents(my_graph, vertex_key) 
    
    if adj_map is None: # If vertex doesn't exist
        return lt.new_list() # Return an empty array_list of keys (for non-existent vertex)
    
    # If adj_map is a map (could be empty), get its key_set
    return map.key_set(adj_map) # This correctly returns an array_list of keys

def get_vertex_info(my_graph, key_u):
    return map.get(my_graph['vertices'], key_u)