# run_prim_tests.py

import traceback # To print full error tracebacks

# Import graph implementation (non-directed for Prim's)
from DataStructures.Graph import no_digraph as g 

# Import necessary list, map, and queue structures
from DataStructures.List import array_list as lt # Used by graph, map
from DataStructures.Stack import stack as stk # Not directly used by Prim, but for general consistency
from DataStructures.Map import map_linear_probing as map # Used by graph, Prim's structures
from DataStructures.Queue import queue as q # Used by Prim's mst_edges_queue

# Import your Prim's algorithm implementation
from DataStructures.Graph import prim as prim_module 

# --- Test Tracking ---
total_tests = 0
passed_tests = 0

def run_test(test_function, test_name):
    global total_tests, passed_tests
    print(f"--- Running Test: {test_name} ---")
    try:
        test_function()
        print(f"PASSED: {test_name}\n")
        passed_tests += 1
    except AssertionError as e:
        print(f"FAILED: {test_name} - {e}\n")
        traceback.print_exc() # Print full traceback for AssertionErrors
    except Exception as e:
        print(f"ERROR: {test_name} - An unexpected error occurred: {e}\n")
        traceback.print_exc() # Print full traceback for ALL other errors
    finally:
        total_tests += 1

# --- Helper function to create graphs for Prim's tests ---
def setup_prim_test_graphs():
    # Graph 1: Simple Connected Graph
    # A --(1)-- B
    # |        /
    # (3)     (1)
    # |      /
    # C --(2)-- D
    # Expected MST: A-B (1), B-C (1), B-D (2). Total weight: 1+1+2=4
    # (Prim might choose A-B or B-C first from B)
    graph_simple_connected = g.new_graph(4, directed=False)
    graph_simple_connected = g.insert_vertex(graph_simple_connected, 'A', 'Node A')
    graph_simple_connected = g.insert_vertex(graph_simple_connected, 'B', 'Node B')
    graph_simple_connected = g.insert_vertex(graph_simple_connected, 'C', 'Node C')
    graph_simple_connected = g.insert_vertex(graph_simple_connected, 'D', 'Node D')
    graph_simple_connected = g.add_edge(graph_simple_connected, 'A', 'B', 1.0)
    graph_simple_connected = g.add_edge(graph_simple_connected, 'A', 'C', 3.0)
    graph_simple_connected = g.add_edge(graph_simple_connected, 'B', 'C', 1.0) # Lower cost for B-C
    graph_simple_connected = g.add_edge(graph_simple_connected, 'B', 'D', 2.0)
    graph_simple_connected = g.add_edge(graph_simple_connected, 'C', 'D', 4.0)

    # Graph 2: Disconnected Graph
    # A --(1)-- B    X --(5)-- Y
    graph_disconnected = g.new_graph(4, directed=False)
    graph_disconnected = g.insert_vertex(graph_disconnected, 'A', 'NA')
    graph_disconnected = g.insert_vertex(graph_disconnected, 'B', 'NB')
    graph_disconnected = g.insert_vertex(graph_disconnected, 'X', 'NX')
    graph_disconnected = g.insert_vertex(graph_disconnected, 'Y', 'NY')
    graph_disconnected = g.add_edge(graph_disconnected, 'A', 'B', 1.0)
    graph_disconnected = g.add_edge(graph_disconnected, 'X', 'Y', 5.0)

    # Graph 3: Single Vertex Graph
    graph_single_vertex = g.new_graph(1, directed=False)
    graph_single_vertex = g.insert_vertex(graph_single_vertex, 'S', 'Solo Node')

    # Graph 4: Empty Graph
    graph_empty = g.new_graph(0, directed=False)

    return graph_simple_connected, graph_disconnected, graph_single_vertex, graph_empty

# --- Test Functions Definitions ---

def test_prim_source_not_found():
    _, _, _, graph_empty = setup_prim_test_graphs()
    try:
        prim_module.prim_mst(graph_empty, 'Z')
        assert False, "Expected ValueError for non-existent source, but none was raised."
    except ValueError as e:
        assert str(e) == "El vértice fuente 'Z' no se encuentra en el grafo.", "Incorrect error message for non-existent source."
    except Exception as e:
        raise AssertionError(f"Expected ValueError, but got {type(e).__name__}: {e}")

def test_prim_on_empty_graph():
    _, _, _, graph_empty = setup_prim_test_graphs()
    # Prim's on an empty graph should technically result in an empty MST.
    # The new_prim_structure is called with order=0, so maps are empty.
    # prim_mst will immediately return an empty structure if source not found,
    # or handle a 0-order graph from its first check.
    try:
        # If order is 0, g.get_vertex_info will raise error if source is anything.
        # If source is actually in graph (which it won't be if order=0), it works.
        # So we expect a ValueError.
        prim_module.prim_mst(graph_empty, 'A')
        assert False, "Expected ValueError for source not found in empty graph, but none was raised."
    except ValueError as e:
        assert str(e) == "El vértice fuente 'A' no se encuentra en el grafo.", "Incorrect error message for source in empty graph."
    except Exception as e:
        raise AssertionError(f"Expected ValueError, but got {type(e).__name__}: {e}")


def test_prim_on_single_vertex_graph():
    _, _, graph_single_vertex, _ = setup_prim_test_graphs()
    search_results = prim_module.prim_mst(graph_single_vertex, 'S')

    # MST should contain 0 edges and total weight 0.0
    assert q.is_empty(search_results['mst_edges_queue']) == True, "MST queue should be empty for single vertex."
    assert prim_module.weight_mst(graph_single_vertex, search_results) == 0.0, "MST weight should be 0.0 for single vertex."


def test_prim_basic_connected_graph():
    graph_simple_connected, _, _, _ = setup_prim_test_graphs()
    search_results = prim_module.prim_mst(graph_simple_connected, 'A') # Start from A

    # Expected MST edges (unordered, but sum and set should match):
    # A-B (1.0), B-C (1.0), B-D (2.0)
    expected_weight = 1.0 + 1.0 + 2.0 # = 4.0
    expected_edges_set = {
        frozenset({'A', 'B'}), 
        frozenset({'B', 'C'}), 
        frozenset({'B', 'D'})
    }

    # Verify total weight
    actual_weight = prim_module.weight_mst(graph_simple_connected, search_results)
    assert actual_weight == expected_weight, \
        f"Incorrect MST total weight. Expected: {expected_weight}, Got: {actual_weight}"

    # Verify MST edges
    mst_edges_queue = prim_module.edges_mst(graph_simple_connected, search_results)
    actual_edges_set = set()
    mst_queue_size = q.size(mst_edges_queue)
    assert mst_queue_size == 3, f"MST should have 3 edges, got {mst_queue_size}."

    # Extract edges from the queue and put them into a set for unordered comparison
    # We must dequeue them temporarily to get the items, then put them back for other potential uses.
    temp_edges_list = []
    while not q.is_empty(mst_edges_queue):
        edge = q.dequeue(mst_edges_queue)
        actual_edges_set.add(frozenset({edge['from'], edge['to']})) # Add frozenset for undirected comparison
        temp_edges_list.append(edge)
    
    # Put edges back into the queue (if needed by other functions, though not required by prompt)
    for edge in temp_edges_list:
        q.enqueue(mst_edges_queue, edge)

    assert actual_edges_set == expected_edges_set, \
        f"Incorrect MST edges. Expected: {expected_edges_set}, Got: {actual_edges_set}"

    # Verify reachability for all nodes in MST (implied by algorithm completion)
    # Check that all nodes are marked as True in search_results['marked']
    all_vertices_in_graph = g.vertices(graph_simple_connected)
    for i in range(lt.size(all_vertices_in_graph)):
        v_key = lt.get_element(all_vertices_in_graph, i)
        assert map.get(search_results['marked'], v_key) == True, \
            f"Vertex '{v_key}' should be marked as part of MST."


def test_prim_disconnected_graph():
    graph_disconnected, _, _, _ = setup_prim_test_graphs()
    search_results = prim_module.prim_mst(graph_disconnected, 'A') # Start from component A-B

    # Expected MST for component A-B: A-B (1.0). Total weight: 1.0
    expected_weight = 1.0
    expected_edges_set = {frozenset({'A', 'B'})}

    # Verify total weight for the component's MST
    actual_weight = prim_module.weight_mst(graph_disconnected, search_results)
    assert actual_weight == expected_weight, \
        f"Incorrect MST total weight for disconnected component. Expected: {expected_weight}, Got: {actual_weight}"

    # Verify MST edges for the component
    mst_edges_queue = prim_module.edges_mst(graph_disconnected, search_results)
    actual_edges_set = set()
    mst_queue_size = q.size(mst_edges_queue)
    assert mst_queue_size == 1, f"MST should have 1 edge, got {mst_queue_size} for disconnected component."

    temp_edges_list = []
    while not q.is_empty(mst_edges_queue):
        edge = q.dequeue(mst_edges_queue)
        actual_edges_set.add(frozenset({edge['from'], edge['to']}))
        temp_edges_list.append(edge)
    for edge in temp_edges_list:
        q.enqueue(mst_edges_queue, edge)

    assert actual_edges_set == expected_edges_set, \
        f"Incorrect MST edges for disconnected component. Expected: {expected_edges_set}, Got: {actual_edges_set}"

    # Verify that only nodes in the component are marked
    assert map.get(search_results['marked'], 'A') == True
    assert map.get(search_results['marked'], 'B') == True
    assert map.get(search_results['marked'], 'X') == False, "X should not be marked in disconnected graph."
    assert map.get(search_results['marked'], 'Y') == False, "Y should not be marked in disconnected graph."


# --- Main execution block ---
if __name__ == "__main__":
    print("===================================")
    print(" Starting Prim's Algorithm Tests ")
    print("===================================\n")

    run_test(test_prim_source_not_found, "Prim: Source Not Found")
    run_test(test_prim_on_empty_graph, "Prim: On Empty Graph")
    run_test(test_prim_on_single_vertex_graph, "Prim: On Single Vertex Graph")
    run_test(test_prim_basic_connected_graph, "Prim: Basic Connected Graph")
    run_test(test_prim_disconnected_graph, "Prim: Disconnected Graph")


    print("===================================")
    print(" Test Summary ")
    print("===================================")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed/Errored: {total_tests - passed_tests}")
    print("===================================\n")

    if passed_tests == total_tests:
        print("All Prim's tests passed successfully!")
    else:
        print("Some Prim's tests failed. Review the output for details.")