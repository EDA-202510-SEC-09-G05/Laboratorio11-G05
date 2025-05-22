from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as ver
import math 
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
        if nodo['key'] == key_u:
            vertex_u = nodo['key']
            
    if vertex_u == None:
        raise Exception("El vertice u no existe")
    
    for nodo in lista_de_adyacencia_info:
        if nodo['key'] == key_v:
            vertex_v = nodo['key']
            
    if vertex_v == None: 
        raise Exception("El vertice v no existe")
    
    adyacencia_u = None
    for nodo in lista_de_adyacencia:
        if nodo['key'] == key_u:
            adyacencia_u = nodo["value"]

    arco = edg.new_edge(key_v,weight) 
    if adyacencia_u != None:   
        map.put(adyacencia_u,key_v,arco)
    my_graph['num_edges']+=1
    
    return my_graph
    
a = new_graph(4)


a = insert_vertex(a,1, {"name": "D"})
b = insert_vertex(a,2, {"name": "Sofia"})
b = insert_vertex(a,3, {"name": "uji"})
c = update_vertex_info(a,2,'a')
d = add_edge(a,1,2,2.0)
d = add_edge(a,1,2,3.0)
d = add_edge(a,2,1,8.0)
d = add_edge(a,1,3,8.0)


#print(d)

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


print(some_graph)

def degree(my_graph,key_u):
    lista_adyacencia_u = map.get(my_graph['vertices'],key_u)
    if lista_adyacencia_u == None:
        raise Exception("El vertice no existe")
    numero = lista_adyacencia_u['adjacents']['size']     
    return numero
z = degree(some_graph,9)
print(z)

