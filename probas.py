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
    
    insert = map.put(my_graph, key_u, new_vertex)
    
    return insert 

a = new_graph(10)
a = insert_vertex(a['vertices'], "Lugar", 4)





print(a)



