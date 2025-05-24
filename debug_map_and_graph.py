# debug_map_and_graph.py (FINAL & CORRECTED VERSION - Copy Entire Content)

# Import the modules directly involved in the suspected bug
from DataStructures.Graph import no_digraph as g # Your non-directed graph
from DataStructures.Map import map_linear_probing as mp # Your map implementation
from DataStructures.List import array_list as lt # Your array_list implementation

print("--- Starting Debugging Script for Map and Graph Adjacencies ---")
print("This script will attempt to recreate the missing adjacency issue.")

# --- Helper function to print map details ---
# This will go deeper than map.key_set to inspect the raw table
def print_map_internal_state(map_obj, map_name="Map"):
    print(f"\n  INTERNAL STATE of '{map_name}':")
    if not isinstance(map_obj, dict) or 'table' not in map_obj or 'elements' not in map_obj['table']:
        print(f"    WARNING: '{map_name}' is not a recognized map object structure.")
        return

    print(f"    Reported size: {mp.size(map_obj)}, Capacity: {map_obj['capacity']}")
    
    # --- Direct scan of the hash table ---
    # Use lt.new_list() and lt.add_last() for custom list operations
    direct_scan_keys_lt = lt.new_list() 
    print(f"    Raw Table Contents (size: {map_obj['capacity']}):")
    for i in range(map_obj['capacity']):
        entry = map_obj['table']['elements'][i]
        
        # --- ROBUSTNESS FIX FOR KeyError: 'state' & Consistent List API ---
        if entry is None:
            print(f"      [{i}]: None")
        elif not isinstance(entry, dict): # Catch unexpected non-dict entries
            print(f"      [{i}]: UNEXPECTED TYPE ({type(entry).__name__}) -> {entry}")
        elif 'state' not in entry: # This is the specific KeyError you were getting!
            print(f"      [{i}]: MISSING_STATE_KEY (key='{entry.get('key', 'N/A')}', value='{entry.get('value', 'N/A')}')")
            # If state is missing but it has a key, assume it's an intended entry for now
            if 'key' in entry: 
                 lt.add_last(direct_scan_keys_lt, entry['key']) # Use lt.add_last()
        elif entry['state'] == 'deleted':
            print(f"      [{i}]: DELETED (key='{entry.get('key', 'N/A')}')")
        elif entry['state'] == 'occupied':
            print(f"      [{i}]: OCCUPIED (key='{entry['key']}', value='{entry['value']}')")
            lt.add_last(direct_scan_keys_lt, entry['key']) # Use lt.add_last()
        
    print(f"    Keys found by direct table scan: {[lt.get_element(direct_scan_keys_lt, i) for i in range(lt.size(direct_scan_keys_lt))]}")

    # --- Call map.key_set() to compare ---
    # Use lt.new_list() and lt.add_last() for custom list operations
    keys_via_keyset_list_lt = lt.new_list() 
    keys_from_keyset = mp.key_set(map_obj) # This is the function called by g.adjacents()
    if keys_from_keyset: # Ensure it's not None
        for i in range(lt.size(keys_from_keyset)):
            lt.add_last(keys_via_keyset_list_lt, lt.get_element(keys_from_keyset, i)) # <--- FIX: Use lt.add_last()
    print(f"    Keys returned by map.key_set(): {[lt.get_element(keys_via_keyset_list_lt, i) for i in range(lt.size(keys_via_keyset_list_lt))]}")

    # --- Assertions for consistency within this debug script ---
    try:
        direct_scan_keys_py = [lt.get_element(direct_scan_keys_lt, i) for i in range(lt.size(direct_scan_keys_lt))]
        keys_via_keyset_list_py = [lt.get_element(keys_via_keyset_list_lt, i) for i in range(lt.size(keys_via_keyset_list_lt))]

        assert mp.size(map_obj) == len(direct_scan_keys_py), \
            f"FAIL: Reported size ({mp.size(map_obj)}) does not match direct scan count ({len(direct_scan_keys_py)})!"
        assert set(direct_scan_keys_py) == set(keys_via_keyset_list_py), \
            f"FAIL: Direct scan keys ({direct_scan_keys_py}) do not match key_set() keys ({keys_via_keyset_list_py})!"
        print(f"  '{map_name}' internal state and key_set() are CONSISTENT.")
    except AssertionError as e:
        print(f"  ERROR: {e}")

# --- Test Case: Recreate branched graph setup and inspect adjacencies ---
print("\n=== Test Case: Branched Graph Adjacency Check ===")
my_graph = g.new_graph(5, directed=False) # Non-directed graph
my_graph = g.insert_vertex(my_graph, 'A', 'Node A')
my_graph = g.insert_vertex(my_graph, 'B', 'Node B')
my_graph = g.insert_vertex(my_graph, 'C', 'Node C')
my_graph = g.insert_vertex(my_graph, 'D', 'Node D')
my_graph = g.insert_vertex(my_graph, 'E', 'Node E')

print("\n--- Step 1: Add edge A-B ---")
my_graph = g.add_edge(my_graph, 'A', 'B', 1)
adj_map_A = mp.get(my_graph['adjacency_list'], 'A')
print_map_internal_state(adj_map_A, "Adj Map for A (after A-B)") # Should show 'B'

print("\n--- Step 2: Add edge A-C ---")
my_graph = g.add_edge(my_graph, 'A', 'C', 1)
adj_map_A = mp.get(my_graph['adjacency_list'], 'A') # Get updated map
print_map_internal_state(adj_map_A, "Adj Map for A (after A-C)") # Should show 'B', 'C'

print("\n--- Step 3: Add edge A-D ---")
my_graph = g.add_edge(my_graph, 'A', 'D', 1)
adj_map_A = mp.get(my_graph['adjacency_list'], 'A')
print_map_internal_state(adj_map_A, "Adj Map for A (after A-D)") # Should show 'B', 'C', 'D'

print("\n--- Step 4: Add edge B-C ---")
my_graph = g.add_edge(my_graph, 'B', 'C', 1)
adj_map_B = mp.get(my_graph['adjacency_list'], 'B')
print_map_internal_state(adj_map_B, "Adj Map for B (after B-C)") # Should show 'A', 'C' (assuming A-B was added and symmetric)

print("\n--- Step 5: Add edge B-E ---")
my_graph = g.add_edge(my_graph, 'B', 'E', 1)
adj_map_B = mp.get(my_graph['adjacency_list'], 'B')
print_map_internal_state(adj_map_B, "Adj Map for B (after B-E)") # Should show 'A', 'C', 'E'

print("\n--- Final Check: Using g.adjacents() ---")
adj_A = g.adjacents(my_graph, 'A')
adj_A_list = [lt.get_element(adj_A, i) for i in range(lt.size(adj_A))]
print(f"Final A neighbors (via g.adjacents()): {adj_A_list}")
try:
    assert 'B' in adj_A_list and 'C' in adj_A_list and 'D' in adj_A_list, "A's neighbors are incomplete!"
    print("A's neighbors: OK")
except AssertionError as e:
    print(f"A's neighbors: FAILED - {e}")

adj_B = g.adjacents(my_graph, 'B')
adj_B_list = [lt.get_element(adj_B, i) for i in range(lt.size(adj_B))]
print(f"Final B neighbors (via g.adjacents()): {adj_B_list}")
try:
    assert 'A' in adj_B_list and 'C' in adj_B_list and 'E' in adj_B_list, "B's neighbors are incomplete!"
    print("B's neighbors: OK")
except AssertionError as e:
    print(f"B's neighbors: FAILED - {e}")

print("\n--- Debugging script finished ---")