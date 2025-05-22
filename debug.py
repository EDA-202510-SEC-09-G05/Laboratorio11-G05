import sys
import types
from DataStructures.Map import map_linear_probing as map_lib
from DataStructures.Graph import digraph as graph_lib # Assuming your graph.py is named graph.py
from DataStructures.Graph import vertex as ver
from DataStructures.Graph import edge as edg

# --- 1. Monkey Patching for Debug Prints ---
# This technique injects print statements into functions without modifying their source code.

def _debug_put_internal(original_func):
    """Wraps _put_internal to add debug prints."""
    def wrapper(my_map, key, value):
        # Condition to focus prints on small adjacency maps (likely the inner problem)
        # Adjust 'capacity < 10' and 'size <= 3' if your internal maps have different characteristics
        is_adj_map_for_debug = (my_map.get('type') == 'PROBE_HASH_MAP' and my_map.get('size',0) <= 3 and my_map.get('capacity',0) < 10 and key != 1) # Exclude outer map and specific keys if needed

        if is_adj_map_for_debug:
            print(f"\n--- DEBUG: _put_internal CALL for inner map (size={my_map.get('size')}, cap={my_map.get('capacity')}) ---", file=sys.stderr)
            print(f"  Attempting to put key={key}, value={value}", file=sys.stderr)

        hash_val = map_lib.mp.hash_value(my_map, key)
        key_already_exists, pos = map_lib.find_slot(my_map, key, hash_val)

        if is_adj_map_for_debug:
            print(f"  DEBUG: find_slot returned: key_already_exists={key_already_exists}, pos={pos}", file=sys.stderr)

        if pos == -1: # This means find_slot couldn't find a spot
            print(f"  DEBUG ERROR: _put_internal could not find slot for key {key} in map capacity {my_map.get('capacity')}. Element LOST?", file=sys.stderr)
            # We still call the original function, but the element might not be put if the original logic fails
            # This 'return' here was in your _put_internal, so we mimic its behavior.
            return original_func(my_map, key, value) # Pass to original for its own handling

        result = original_func(my_map, key, value) # Call the original function

        if is_adj_map_for_debug:
            if not key_already_exists:
                print(f"  DEBUG: NEW insertion for key {key}. New size={my_map.get('size')}", file=sys.stderr)
            else:
                print(f"  DEBUG: UPDATE for key {key}. Size remains {my_map.get('size')}", file=sys.stderr)
            print(f"  DEBUG: Current map elements: {[map_lib.me.get_key(e) for e in my_map['table']['elements'] if map_lib.me.get_key(e) is not None and map_lib.me.get_key(e) != '__EMPTY__']}", file=sys.stderr)
            
        return result
    return wrapper

def _debug_rehash(original_func):
    """Wraps rehash to add debug prints."""
    def wrapper(my_map):
        is_adj_map_for_debug = (my_map.get('type') == 'PROBE_HASH_MAP' and my_map.get('size',0) <= 3 and my_map.get('capacity',0) < 10)

        if is_adj_map_for_debug:
            print(f"\n--- DEBUG: REHASHING map (old_size={my_map.get('size')}, old_capacity={my_map.get('capacity')}) ---", file=sys.stderr)
        
        # Capture old elements before rehash for verification
        old_keys = [map_lib.me.get_key(e) for e in my_map['table']['elements'] if map_lib.me.get_key(e) is not None and map_lib.me.get_key(e) != '__EMPTY__']
        if is_adj_map_for_debug:
             print(f"  DEBUG: Elements before rehash: {old_keys}", file=sys.stderr)

        new_map_obj = original_func(my_map) # Call the original rehash function

        if is_adj_map_for_debug:
            print(f"--- DEBUG: REHASH COMPLETE: new_size={new_map_obj.get('size')}, new_capacity={new_map_obj.get('capacity')} ---", file=sys.stderr)
            new_keys = [map_lib.me.get_key(e) for e in new_map_obj['table']['elements'] if map_lib.me.get_key(e) is not None and map_lib.me.get_key(e) != '__EMPTY__']
            print(f"  DEBUG: Elements after rehash: {new_keys}", file=sys.stderr)
            lost_keys = set(old_keys) - set(new_keys)
            if lost_keys:
                print(f"  DEBUG WARNING: Keys lost during rehash: {lost_keys}", file=sys.stderr)

        return new_map_obj
    return wrapper

# Apply the patches to your map_linear_probing module
map_lib._put_internal = _debug_put_internal(map_lib._put_internal)
map_lib.rehash = _debug_rehash(map_lib.rehash)


# --- 2. Your Original Test Code (with the add_edge fix) ---
# Copy and paste your test sequence directly here.
# Make sure to include the corrected add_edge function from the previous step.

def new_graph (order, directed=False):
    
    graph = { "directed": directed,
             "order": order, 
             "num_edges":0,
             "vertices": None,
             "adjacency_list": None}


    graph["vertices"] = map_lib.new_map(order, 0.5)
    graph ["adjacency_list"] = map_lib.new_map(order, 0.5)
    
    return graph 


def insert_vertex (my_graph, key_u,info_u):
        

    new_vertex = ver.new_vertex(key_u, info_u)

    # When you insert a vertex, its adjacency list should be an empty map
    # that your map_linear_probing can handle.
    # The default new_vertex creates 'adjacents' as a map, so this should be fine.
    
    lista_de_adyacencia = map_lib.put(my_graph['adjacency_list'], new_vertex['key'], new_vertex['adjacents'])
    lista_info_nodo = map_lib.put(my_graph['vertices'], new_vertex['key'], new_vertex['value'])
    
    
    my_graph['adjacency_list'] = lista_de_adyacencia
    my_graph['vertices'] = lista_info_nodo
 
    
    return my_graph 


def update_vertex_info (my_graph, key_u, new_info_u):
    
    vertex = map_lib.get(my_graph['vertices'], key_u)
    
    if vertex is None:
        return None
    else:
        # Direct modification is okay if you're sure of the internal structure
        # A more robust way might be: my_graph['vertices'] = map_lib.put(my_graph['vertices'], key_u, new_info_u)
        # But for 'update_vertex_info' where 'value' is a simple info, this could work.
        # However, for a map_entry, 'value' might be directly accessible as 'value' key.
        # Let's assume your 'map_entry' allows direct modification via 'value' key.
        lista_adyacencia = my_graph['vertices']['table']['elements']
        for nodo in lista_adyacencia:
            if nodo is not None and nodo['key'] == key_u: # Add 'is not None'
                nodo['value'] = new_info_u
                break # Exit after finding and updating
    
    return my_graph

def add_edge (my_graph,key_u, key_v, weight):
    vertex_u = None
    vertex_v = None
    lista_de_adyacencia_info = my_graph['vertices']['table']['elements']
    
    # Find vertex_u's key
    for nodo in lista_de_adyacencia_info:
        if nodo is not None and nodo['key'] == key_u: 
            vertex_u = nodo['key']
            break 
            
    if vertex_u == None:
        raise Exception(f"El vertice u ({key_u}) no existe")
    
    # Find vertex_v's key
    for nodo in lista_de_adyacencia_info:
        if nodo is not None and nodo['key'] == key_v: 
            vertex_v = nodo['key']
            break 
            
    if vertex_v == None: 
        raise Exception(f"El vertice v ({key_v}) no existe")
    
    # Get the *actual* adjacency map object for key_u from the top-level adjacency_list map
    adyacencia_u_map_obj = map_lib.get(my_graph['adjacency_list'], key_u)

    if adyacencia_u_map_obj is None:
        raise Exception(f"Adjacency map for vertex {key_u} not found in main adjacency_list. This should be initialized by insert_vertex.")

    arco = edg.new_edge(key_v,weight) 
    
    # --- CRITICAL FIX IMPLEMENTED HERE (as discussed) ---
    updated_adyacencia_u_map_obj = map_lib.put(adyacencia_u_map_obj, key_v, arco)
    
    my_graph['adjacency_list'] = map_lib.put(my_graph['adjacency_list'], key_u, updated_adyacencia_u_map_obj)
    # --- END CRITICAL FIX ---

    my_graph['num_edges']+=1
    
    return my_graph
    
# Your original test sequence starts here
a = new_graph(6)

a = insert_vertex(a,1, {"name": "D"})
a = insert_vertex(a,2, {"name": "Sofia"}) # Changed 'b' to 'a' to keep graph reference consistent
a = insert_vertex(a,3, {"name": "Pablo "}) # Changed 'b' to 'a'
a = insert_vertex(a,4, {"name": "I"}) # Changed 'b' to 'a'
a = insert_vertex(a,5, {"name": "Y"}) # Changed 'b' to 'a'
a = insert_vertex(a,6, {"name": "T"}) # Changed 'b' to 'a'

# Changed 'c' to 'a' to keep graph reference consistent
a = update_vertex_info(a,2,'a') 

# Changed 'd' to 'a' to keep graph reference consistent
a = add_edge(a,1,2,2.0)
a = add_edge(a,1,2,4.0) # This will overwrite the previous (1,2) edge in the inner map
a = add_edge(a,1,3,9.0) # THIS IS THE EDGE WE ARE DEBUGGING
a = add_edge(a,1,4,2.0)

print("\n--- Final Graph State ---")
print(a) # Print the whole graph

print("\n--- After all add_edge calls (Specific Checks) ---")
# Get the adjacency map for vertex 1
adj_map_for_1 = map_lib.get(a['adjacency_list'], 1)

if adj_map_for_1:
    print(f"Adjacency map for vertex 1: {adj_map_for_1}")
    print(f"Size of adjacency map for vertex 1: {map_lib.size(adj_map_for_1)}")
    
    # Try to get each specific adjacent vertex
    edge_to_2 = map_lib.get(adj_map_for_1, 2)
    edge_to_3 = map_lib.get(adj_map_for_1, 3)
    edge_to_4 = map_lib.get(adj_map_for_1, 4)

    print(f"Edge to vertex 2: {edge_to_2}")
    print(f"Edge to vertex 3: {edge_to_3}")
    print(f"Edge to vertex 4: {edge_to_4}")
else:
    print("Adjacency map for vertex 1 not found (ERROR in graph setup?).")

# You can also inspect the keys of the inner map
if adj_map_for_1:
    keys_of_adj_1 = map_lib.key_set(adj_map_for_1)
    # The key_set method returns a map_lib.lt.new_list() structure.
    # Access its 'elements' key to see the actual list of keys.
    print(f"Keys in adjacency map for vertex 1: {keys_of_adj_1['elements']}") 


# --- Other functions from your original probas.py for completeness ---
def setup_tests():
    empty_graph = new_graph(0)
    some_graph = new_graph(2)

    vertex_1 = ver.new_vertex(1, {"name": "A"})
    vertex_2 = ver.new_vertex(2, {"name": "B"})

    ver.add_adjacent(vertex_1, 2, 3.0) # This modifies the vertex directly, not using map_lib.put
    ver.add_adjacent(vertex_2, 1, 3.0)

    # These are not directly impacting the 1->3 edge debug, but ensure they use your map.put
    some_graph["vertices"] = map_lib.put(some_graph["vertices"], 1, vertex_1) # Ensure correct assignment back
    some_graph["vertices"] = map_lib.put(some_graph["vertices"], 2, vertex_2) # Ensure correct assignment back
    some_graph["num_edges"] = 2 # This might be incorrect if edges are added via add_edge, not directly set

    # IMPORTANT: The adjacency_list for some_graph's vertices also needs to be populated.
    # Your insert_vertex already does this, but setup_tests is bypassing it.
    # For a fully consistent graph, you'd want to use add_edge here too, or ensure insert_vertex
    # also populates the adjacency list map with the vertex's initial empty adjacency map.
    # The current setup_tests manually sets num_edges and vertices, which might not be consistent
    # with how insert_vertex/add_edge manage the adjacency_list.
    # For debugging the 1->3 edge, focus on the 'a' graph, not 'some_graph' for now.

    return empty_graph, some_graph

# empty_graph, some_graph = setup_tests() # Uncomment if you want to run these tests

def vertices(my_graph):
    vertice = map_lib.lt.new_list()
    # It's better to use map_lib.key_set for this, as it iterates over the map's contents reliably
    keys = map_lib.key_set(my_graph['vertices'])
    # Assuming map_lib.key_set returns a map_lib.lt.new_list() object
    return keys 


def degree(my_graph,key_u):
    # Get the specific adjacency map for vertex key_u
    lista_adyacencia_u_map = map_lib.get(my_graph['adjacency_list'],key_u)
    if lista_adyacencia_u_map == None:
        raise Exception("El vertice no existe o no tiene lista de adyacencia")
    # The degree is the size of that inner adjacency map
    numero = map_lib.size(lista_adyacencia_u_map)
    
    return numero

# Example of using degree
# z = degree(a,1) # Use 'a' if you want to test the graph with edges
# print(f"Degree of vertex 1: {z}")