from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as ver
import math 
from DataStructures.Graph import edge as edg
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Graph import digraph as g
from DataStructures.Graph import dijkstra as dijks



def new_graph (order, directed=False):
    
    graph = { "directed": directed,
             "order": order, 
             "num_edges":0,
             "vertices": None,
             "adjacency_list": None}


    graph["vertices"] = map.new_map(order, 0.5)
    graph ["adjacency_list"] = map.new_map(order, 0.5)
    
    return graph 


def insert_vertex (my_graph, key_u,info_u):
        

    new_vertex = ver.new_vertex(key_u, info_u)

    
    lista_de_adyacencia = map.put(my_graph['adjacency_list'],new_vertex['key'], new_vertex['adjacents'])
    lista_info_nodo = map.put(my_graph['vertices'],new_vertex['key'],new_vertex['value'])
    
    
    my_graph['adjacency_list'] = lista_de_adyacencia
    my_graph['vertices'] = lista_info_nodo
 
    
    return my_graph 


def update_vertex_info (my_graph, key_u, new_info_u):
    
    vertex = map.get(my_graph['vertices'], key_u)
    
    if vertex is None:
        return None
    else:
        lista_adyacencia = my_graph['vertices']['table']['elements']
        for nodo in lista_adyacencia:
            if key_u == nodo['key']:
                nodo['value'] = new_info_u
    
    return my_graph

def add_edge (my_graph,key_u, key_v, weight):
    vertex_u = None
    vertex_v = None
    lista_de_adyacencia_info = my_graph['vertices']['table']['elements']
    lista_de_adyacencia = my_graph['adjacency_list']['table']['elements'] 
    
    
    for nodo in lista_de_adyacencia_info:
        if nodo is not None and nodo['key'] == key_u: 
            vertex_u = nodo['key']
            break 
            
    if vertex_u == None:
        raise Exception("El vertice u no existe") 
    
    for nodo in lista_de_adyacencia_info:
        if nodo is not None and nodo['key'] == key_v: 
            vertex_v = nodo['key']
            break 
            
    if vertex_v == None: 
        raise Exception("El vertice v no existe") 
    
    adyacencia_u = None
    
    for nodo in lista_de_adyacencia:
        if nodo is not None and nodo['key'] == key_u: 
            adyacencia_u = nodo["value"] 
            break 

    arco = edg.new_edge(key_v,weight) 
    
    #Esta parte me sirvio para hacer debugging hecha con gemini la verdad pa q digo q no. 
    # --- MAJOR LOGIC CHANGES START HERE ---
    if adyacencia_u is not None: # Changed from '!= None' to 'is not None' (Pythonic)
        # 1. Call map.put on the inner adjacency map (`adyacencia_u`).
        # This call RETURNS the updated map. If a rehash occurred, it's a NEW map object.
        updated_adyacencia_u_map_obj = map.put(adyacencia_u, key_v, arco)
        
        # 2. Now, take this `updated_adyacencia_u_map_obj` (which might be a new object
        # if the inner map rehashed) and put it back into the TOP-LEVEL
        # `my_graph['adjacency_list']` map for the given `key_u`.
        # This ensures the main graph's adjacency list always references the correct,
        # up-to-date inner map for vertex `key_u`.
        # The `map.put` on the top-level map also handles its own potential rehash.
        my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, updated_adyacencia_u_map_obj)
    # --- MAJOR LOGIC CHANGES END HERE ---

    my_graph['num_edges']+=1
    
    return my_graph
    
a = new_graph(6)



#d = add_edge(a,1,2,4.0) 
#d = add_edge(a,1,3,9.0)
#d = add_edge(a,1,4,2.0)
#d = add_edge(a,1,4,2.0)
#d = add_edge(a,2,4,2.0)
#d = add_edge(a,2,3,2.0)
#d = add_edge(a,4,3,2.0)

#lista = map.get(d['adjacency_list'],4)
#nodod_adyacentes_1 = map.key_set(lista)
#print(lista['table']['elements'])
#print(nodod_adyacentes_1)
#print(d)
'''
print("\n--- After all add_edge calls ---")
# Get the adjacency map for vertex 1
adj_map_for_1 = map.get(d['adjacency_list'], 1)

if adj_map_for_1:
    print(f"Adjacency map for vertex 1: {adj_map_for_1}")
    print(f"Size of adjacency map for vertex 1: {map.size(adj_map_for_1)}")
    
    # Try to get each specific adjacent vertex
    edge_to_2 = map.get(adj_map_for_1, 2)
    edge_to_3 = map.get(adj_map_for_1, 3)
    edge_to_4 = map.get(adj_map_for_1, 4)

    print(f"Edge to vertex 2: {edge_to_2}")
    print(f"Edge to vertex 3: {edge_to_3}")
    print(f"Edge to vertex 4: {edge_to_4}")
else:
    print("Adjacency map for vertex 1 not found.")

# You can also inspect the keys of the inner map
if adj_map_for_1:
    keys_of_adj_1 = map.key_set(adj_map_for_1)
    print(f"Keys in adjacency map for vertex 1: {keys_of_adj_1['elements']}") # Assuming key_set returns a list-like object

'''


def setup_tests():
    empty_graph = new_graph(0)
    some_graph = new_graph(2)

    vertex_1 = ver.new_vertex(1, {"name": "A"})
    vertex_2 = ver.new_vertex(2, {"name": "B"})

    ver.add_adjacent(vertex_1, 2, 3.0)
    ver.add_adjacent(vertex_2, 1, 3.0)

    vertex_1 = map.put(some_graph["vertices"], 1, vertex_1)
    vertex_2 = map.put(some_graph["vertices"], 2, vertex_2)
    some_graph["num_edges"] = 2

    return empty_graph, some_graph

empty_graph, some_graph = setup_tests()

#m = insert_vertex(some_graph, 3, {"name": "D"})
#m = add_edge(some_graph, 1, 3, 3.0)

#print(m)

def vertices(my_graph):
    vertice = lt.new_list()
    lista_de_adyacencia_info = my_graph['vertices']['table']['elements']
    
    for nodo in lista_de_adyacencia_info:
        if nodo['key'] != None:
            lt.add_last(vertice, nodo['key'])
    
    return vertice

def degree(my_graph,key_u):
    lista_adyacencia_u = map.get(my_graph['adjacency_list'],key_u)
    if lista_adyacencia_u == None:
        raise Exception("El vertice no existe")
    numero = lista_adyacencia_u['size']
    
    return numero


#print(some_graph)

def degree(my_graph,key_u):
    lista_adyacencia_u = map.get(my_graph['vertices'],key_u)
    if lista_adyacencia_u == None:
        raise Exception("El vertice no existe")
    numero = lista_adyacencia_u['adjacents']['size']     
    return numero

z = degree(some_graph,1)
#print(z)


def get_vertex(my_graph,key_u):
    lista_adyacencia = my_graph['vertices']['table']['elements']
    for nodo in lista_adyacencia:
        if nodo["key"] == key_u:
            return nodo

    raise Exception("El vertice no existe")

#m = get_vertex(d,1)
#print('\n'*2, m)


def new_dijsktra_structure(source, g_order):
    """

    Crea una estructura de busqueda usada en el algoritmo **dijsktra**.

    Se crea una estructura de busqueda con los siguientes atributos:

    - **source**: Vertice de origen. Se inicializa en ``source``
    - **visited**: Mapa con los vertices visitados. Se inicializa en ``None``
    - **pq**: Cola indexada con los vertices visitados. Se inicializa en ``None``

    :returns: Estructura de busqueda
    :rtype: dijsktra_search
    """
    structure = {
        "source": source,
        "visited": map.new_map(
            g_order, 0.5),
        "pq": pq.new_heap()}
    
    
    
    g_order = g.order(source)
    structure['edge_to'] = map.new_map(num_elements=g_order, load_factor=0.5)
    structure['dist_to'] = map.new_map(num_elements= g_order, load_factor=0.5)
    structure['marked'] = map.new_map(num_elements= g_order, load_factor=0.5)
    vertices = g.vertices(source)
    for i in range(lt.size(vertices)):
        vert = lt.get_element(vertices, i)
    map.put(structure['dist_to'], vert, float('inf'))
    map.put(structure['marked'], vert, False)
    structure['pq'] = pq.new_heap(is_min_pq=True)
    
    
    
    return structure

a = insert_vertex(a,1, {"name": "D"})
b = insert_vertex(a,2, {"name": "Sofia"})
b = insert_vertex(a,3, {"name": "Pablo "})
b = insert_vertex(a,4, {"name": "I"})
b = insert_vertex(a,5, {"name": "Y"})
b = insert_vertex(a,6, {"name": "T"})
c = update_vertex_info(a,2,'a')
d = add_edge(a,1,2,2.0)

r = dijks.dijkstra(d,1)

ml = dijks.has_path_to(2,r)
print(r)
