
from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import digraph as g 
from DataStructures.Graph import edge as edg 
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Graph import dijsktra_structure as ds 
import math 

def dijkstra(my_graph, source_key):
    """
    Implementa el algoritmo de Dijkstra para encontrar los caminos más cortos desde un origen.

    Args:
        my_graph: El grafo de búsqueda (diccionario) sobre el cual se ejecutará el algoritmo.
        source_key: La clave del vértice de inicio.

    Returns:
        Un diccionario que representa la estructura de búsqueda de Dijkstra
        con las distancias y caminos más cortos calculados.
    Raises:
        Exception: Si el vértice de origen no existe en el grafo.
    """
    
    # 1. Validate source vertex existence in the graph
    if map.get(my_graph['vertices'], source_key) is None:
        raise Exception(f"El vertice de origen {source_key} no existe en el grafo.")

    # 2. Get graph order (total number of vertices) and initialize structure
    graph_order = g.order(my_graph) # Use g.order from your digraph.py
    aux_structure = ds.new_dijsktra_structure(source_key, graph_order)

    # 3. Initialize distances for all vertices and mark them as unvisited
    all_vertex_keys = g.vertices(my_graph) # Use g.vertices from your digraph.py
    for i in range(lt.size(all_vertex_keys)):
        vert_key = lt.get_element(all_vertex_keys, i)
        map.put(aux_structure['dist_to'], vert_key, float('inf'))
        map.put(aux_structure['marked'], vert_key, False)
        # edge_to entries are left as None/empty until a path is discovered

    # 4. Set the distance from the source vertex to itself as 0.0
    map.put(aux_structure['dist_to'], source_key, 0.0)
    
    # 5. Add the source vertex to the priority queue with its initial distance (0.0)
    # The pq.put function expects (priority_value, item_value)
    pq.put(aux_structure['pq'], 0.0, source_key) 

    # 6. Main Dijkstra's Algorithm Loop
    while not pq.is_empty(aux_structure['pq']):
        # Extract the vertex 'u_key' with the smallest distance from the priority queue
        # pq.del_min returns (priority_value, item_value)
        current_dist_from_pq, u_key = pq.del_min(aux_structure['pq'])

        # If the vertex 'u_key' has already been marked (processed/finalized), skip it.
        # This is crucial for handling stale entries in the priority queue.
        if map.get(aux_structure['marked'], u_key):
            continue

        # Mark the current vertex 'u_key' as visited (finalized)
        map.put(aux_structure['marked'], u_key, True)

        # Get the adjacency list (map) for the current vertex 'u_key'
        # Use g.get_adjacencies from your digraph.py
        adj_map_for_u = g.get_adjacencies(my_graph, u_key)
        
        # Iterate over neighbors 'v_key' of 'u_key' to relax edges
        # map.key_set returns an array_list of keys from the given map
        adj_keys = map.key_set(adj_map_for_u)
        for i in range(lt.size(adj_keys)):
            v_key = lt.get_element(adj_keys, i) # This is the target vertex key (neighbor)
            edge_obj = map.get(adj_map_for_u, v_key) # Get the edge object itself (e.g., {'to': v_key, 'weight': X})
            
            # Ensure edge_obj is valid and has a 'weight' attribute/key
            if edge_obj is None or 'weight' not in edge_obj: 
                # This could happen if your map.key_set returns keys for empty/invalid slots,
                # or if edge objects aren't consistently structured.
                continue 
            
            weight = edge_obj['weight'] # Access the weight from the edge dictionary/object

            # Relaxation step: If a shorter path to 'v_key' is found through 'u_key'
            dist_u = map.get(aux_structure['dist_to'], u_key)
            dist_v = map.get(aux_structure['dist_to'], v_key)

            if dist_u + weight < dist_v:
                # Update distance to 'v_key'
                map.put(aux_structure['dist_to'], v_key, dist_u + weight)
                # Set 'u_key' as the predecessor for 'v_key' in the shortest path
                map.put(aux_structure['edge_to'], v_key, u_key)
                # Add or update 'v_key' in the priority queue with its new, shorter distance
                pq.put(aux_structure['pq'], dist_u + weight, v_key)

    # Dijkstra's algorithm returns the populated auxiliary structure
    return aux_structure

# --- Helper functions to query Dijkstra's results ---

def dist_to(key_v, aux_structure):
    """
    Retorna el costo para llegar del vértice source al vértice key_v.

    Args:
        key_v: La clave del vértice destino.
        aux_structure: La estructura de búsqueda de Dijkstra (resultado de dijkstra()).

    Returns:
        El costo total para llegar de source a key_v (un float).
        `float('inf')` si no existe camino o el vértice no es alcanzable.
    Raises:
        Exception: Si el vértice destino `key_v` no existe en la estructura de búsqueda
                   (es decir, no era un vértice en el grafo procesado).
    """
    distance = map.get(aux_structure['dist_to'], key_v)
    if distance is None:
        # This implies key_v was not a vertex in the graph when Dijkstra was run.
        raise Exception(f"El vertice destino {key_v} no existe en la estructura de búsqueda.")
    return distance

def has_path_to(key_v, aux_structure):
    """
    Indica si hay camino entre source y key_v.

    Args:
        key_v: La clave del vértice de destino.
        aux_structure: La estructura de búsqueda de Dijkstra (resultado de dijkstra()).

    Returns:
        True si existe camino, False de lo contrario.
    Raises:
        Exception: Si el vértice de destino `key_v` no existe en la estructura de búsqueda.
    """
    # A path exists if its distance is not infinity AND it was marked (meaning it was reachable)
    distance = dist_to(key_v, aux_structure) # Use dist_to to handle vertex existence check
    return distance != float('inf') and map.get(aux_structure['marked'], key_v)

def path_to(key_v, aux_structure):
    """
    Retorna el camino entre source y key_v en un array_list (actuando como pila).

    Args:
        key_v: La clave del vértice de destino.
        aux_structure: La estructura de búsqueda de Dijkstra (resultado de dijkstra()).

    Returns:
        Un array_list con las claves de los vértices en el camino desde source hasta key_v,
        o `None` si no hay camino.
    Raises:
        Exception: Si el vértice de destino `key_v` no existe en la estructura de búsqueda.
    """
    if not has_path_to(key_v, aux_structure):
        return None # No path exists

    path_list = lt.new_list() # Use array_list to build the path
    current_vertex = key_v

    # Reconstruct path by traversing edge_to backwards from destination to source
    while current_vertex != aux_structure['source']:
        # Defensive check: if current_vertex becomes None before reaching source,
        # it indicates a broken path in edge_to, which shouldn't happen if has_path_to is True.
        if current_vertex is None: 
            raise Exception(f"Error interno: Reconstrucción de camino rota para {key_v}.")
        
        # Add to the front of the list to maintain correct path order
        lt.add_first(path_list, current_vertex) 
        
        # Move to the predecessor vertex
        current_vertex = map.get(aux_structure['edge_to'], current_vertex)
        
    # Add the source vertex at the very beginning of the path
    lt.add_first(path_list, aux_structure['source']) 

    return path_list

