from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as ver


def new_graph (order, directed=False):
    
    graph = { "directed": directed,
             "order": order, 
             "num_edges":0,
             "vertices": None,
             "adjacency_list": None}


    graph["vertices"] = map.new_map(order, 0.5)
    graph ["adjacency_list"] = lt.new_list()
    
    return graph 


def insert_vertex (my_graph, key_u,info_u):
        

    new_vertex = ver.new_vertex(key_u, info_u)
    
    insert = map.put(my_graph['vertices'], key_u, new_vertex)
    
    return insert 

def update_vertex_info (my_graph, key_u, new_info_u):
    
    vertex = map.get(my_graph, key_u)
    
    if vertex is None:
        return None
    else:
        ver.set_value(vertex,new_info_u)
        return my_graph
        

def remove_vertex(my_graph, key_u):
    # 1) obtengo posición y abortar si no existe
    pos = map.get(my_graph['vertices'], key_u)
    if pos is None:
        return None

    # 2) elimino el vértice del mapa y de la lista de adyacencia
    map.remove(my_graph['vertices'], key_u)
    lt.delete_element(my_graph['adjacency_list'], pos)

    # 3) quito todas las aristas hacia key_u
    for adj in my_graph['adjacency_list']:
        # mientras aparezca key_u en la lista, la borro
        p = lt.is_present(adj, key_u)
        while p > 0:
            lt.delete_element(adj, p)
            p = lt.is_present(adj, key_u)

    # 4) corrijo las posiciones desplazadas
    for k in map.key_set(my_graph['vertices']):
        p = map.get(my_graph['vertices'], k)
        if p > pos:
            map.put(my_graph['vertices'], k, p - 1)

    # 5) actualizo contadores
    my_graph['num_vertices'] -= 1
    # recuento total de aristas tras la limpieza
    total = 0
    for adj in my_graph['adjacency_list']:
        total += lt.size(adj)
    my_graph['num_edges'] = total

    return my_graph

        

def add_edge (my_graph,key_u, key_v, weight=1.0):
    
    vertex_u = map.get(my_graph, key_u)
    vertex_v = map.get(my_graph, key_v)
    
    if vertex_u is None or vertex_v is None:
        return None
    else:
        ver.add_adjacent(vertex_u, key_v, weight)
        ver.add_adjacent(vertex_v, key_u, weight)
        my_graph["num_edges"] += 1
        return my_graph
    

def order (my_graph):
    
    return my_graph["size"]


def size (my_graph):
    
    return my_graph["num_edges"]

def vertices (my_graph):
    
    return map.key_set(my_graph["vertices"])

def degree (my_graph, key_u):
    
    vertex = map.get (my_graph, key_u)
    
    if vertex is None:
         raise Exception("El vertice no existe")
    else:
        return ver.degree(vertex)
        
    
def get_edge (my_graph, key_u, key_v):
    
    vertex_u = map.get(my_graph, key_u)
    
    if vertex_u is None:
        raise Exception("El vertice u no existe")
    else:
        edge = ver.get_edge(vertex_u, key_v)
        
        if edge is None:
            return None
        
        return edge 
    

def get_vertex_information (my_graph, key_u):
    
    vertex = map.get(my_graph, key_u)
    
    if vertex is None:
        
        raise Exception("El vertice no existe")
    
    else:
        return ver.get_value(vertex)
    

def contains_vertex (my_graph, key_u):
    
    vertex = map.get(my_graph, key_u)
    
    if vertex is None:
        return False
    else:
        return True
    

def adjacents (my_graph, key_u):
    
    vertex = map.get(my_graph, key_u)
    
    if vertex is None:
        
        raise Exception("El vertice no existe")
    
    else:
        vertex_adjacents = ver.get_adjacents(vertex)
        return map.value_set(vertex_adjacents)
    


"edges_vertex"


def get_vertex (my_graph, key_u):
    
    vertex = map.get(my_graph, key_u)
    
    if vertex is None:
        
        raise Exception("El vertice no existe")
    
    else:
        
        return vertex 
        
        
    
        
                
        
        
        
        
        
        
       
    
    