from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as ver
from DataStructures.Graph import edge as edg


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

def order(my_graph):
    return my_graph['order']

def size(my_graph):
    return my_graph['num_edges']

def vertices(my_graph):
    vertice = lt.new_list()
    lista_de_adyacencia_info = my_graph['vertices']['table']['elements']
    
    for nodo in lista_de_adyacencia_info:
        if nodo['key'] != None:
            lt.add_last(vertice, nodo['key'])
    
    return vertice

def degree_verdadera(my_graph,key_u):
    lista_adyacencia_u = map.get(my_graph['adjacency_list'],key_u)
    if lista_adyacencia_u == None:
        raise Exception("El vertice no existe")
    numero = lista_adyacencia_u['size']
    
    return numero


def degree(my_graph,key_u):
    lista_adyacencia_u = map.get(my_graph['vertices'],key_u)
    if lista_adyacencia_u == None:
        raise Exception("El vertice no existe")
    numero = lista_adyacencia_u['adjacents']['size']     
    return numero

