# File: test_dijkstra_debug.py

# Import your graph functions
from DataStructures.Graph import digraph as g

# Import the DEBUG version of Dijkstra's functions
from DataStructures.Graph import dijkstra_debug as djk # <<< Changed import
from DataStructures.Graph import dijsktra_structure as ds 

# Import the DEBUG version of Map
from DataStructures.Map import map_linear_probing_debug as map # <<< Changed import

# Import other necessary modules
from DataStructures.List import array_list as lt
import math

print("--- Starting Dijkstra Debug Test ---")

# 1. Create a Sample Graph
print("\n1. Creating a sample graph...")
my_graph = g.new_graph(order=6, directed=True) 

# 2. Insert Vertices
print("2. Inserting vertices...")
my_graph = g.insert_vertex(my_graph, 1, "A")
my_graph = g.insert_vertex(my_graph, 2, "B")
my_graph = g.insert_vertex(my_graph, 3, "C")
my_graph = g.insert_vertex(my_graph, 4, "D")
my_graph = g.insert_vertex(my_graph, 5, "E")
my_graph = g.insert_vertex(my_graph, 6, "F")

print(f"Graph order: {g.order(my_graph)}")

graph_vertices = g.vertices(my_graph)
print("Graph vertices: [", end="")
for i in range(lt.size(graph_vertices)):
    print(lt.get_element(graph_vertices, i), end="")
    if i < lt.size(graph_vertices) - 1:
        print(", ", end="")
print("]")

# 3. Add Edges
print("\n3. Adding edges...")
my_graph = g.add_edge(my_graph, 1, 2, 7.0)
my_graph = g.add_edge(my_graph, 1, 3, 9.0)
my_graph = g.add_edge(my_graph, 1, 6, 14.0)
my_graph = g.add_edge(my_graph, 2, 3, 10.0)
my_graph = g.add_edge(my_graph, 2, 4, 15.0)
my_graph = g.add_edge(my_graph, 3, 4, 11.0)
my_graph = g.add_edge(my_graph, 3, 6, 2.0)
my_graph = g.add_edge(my_graph, 4, 5, 6.0)
my_graph = g.add_edge(my_graph, 6, 5, 9.0)

print(f"Graph size (number of edges): {g.size(my_graph)}")


# 4. Run Dijkstra's Algorithm
source_vertex_key = 1
print(f"\n4. Running Dijkstra from source vertex {source_vertex_key}...")
try:
    dijkstra_results = djk.dijkstra(my_graph, source_vertex_key)
    print("\nDijkstra's algorithm executed successfully.")

    # 5. Query Results
    print("\n5. Querying Dijkstra results:")
    
    target_vertices = [1, 2, 3, 4, 5, 6, 99] 
    for target_key in target_vertices:
        try:
            distance = djk.dist_to(target_key, dijkstra_results)
            path_exists = djk.has_path_to(target_key, dijkstra_results) # This call will now print DEBUG_DIJKSTRA_PATH
            
            print(f"  Distance from {source_vertex_key} to {target_key}: {distance} (Path exists: {path_exists})")

            if path_exists:
                path = djk.path_to(target_key, dijkstra_results) # This call will now print DEBUG_DIJKSTRA_PATH
                
                print(f"    Path to {target_key}: [", end="")
                for i in range(lt.size(path)):
                    print(lt.get_element(path, i), end="")
                    if i < lt.size(path) - 1:
                        print(" -> ", end="") 
                print("]")
                
        except Exception as e:
            print(f"  Error querying for vertex {target_key}: {e}")

except Exception as e:
    print(f"\nERROR: Dijkstra's algorithm failed: {e}")

print("\n--- Dijkstra Debug Test Finished ---")