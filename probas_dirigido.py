from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as ver
from DataStructures.Graph import edge as edg # Assuming edg.new_edge(key, weight) exists
from DataStructures.Graph import digraph as g



a = g.new_graph(10)
b = g.insert_vertex(a,'si',"AJA THATS MY SHIT")
b = g.insert_vertex(a,'no',"mucho texto")
b = g.insert_vertex(a,'Pablo',{'codigo':2023,
                             'Altura': 1.85})
b = g.insert_vertex(a,'martin',{'codigo':2024,
                             'Altura': 1.75})
b = g.insert_vertex(a,'Tomi',{'codigo':2022,
                             'Altura': 1.65})

d = g.add_edge(a,"si","no",3.0)
d = g.add_edge(a,"no","si",4.4)
d = g.add_edge(a,'Pablo','martin',9)
d = g.add_edge(a,"martin", 'Pablo',1)
d = g.add_edge(a,"Pablo",'Tomi', 100)

#print(d)

z = map.key_set(a['vertices'])

final = {}
for llave in z['elements']:
    lda = map.get(d['adjacency_list'],llave)
    for adj in lda['table']['elements']:
        if adj is not None and llave not in final:
            final[llave] = [adj['key']]
        elif adj is not None and llave in final:
            final[llave].append(adj["key"])


        
            
        
for llave in final:
    for adj in final[llave]:
        if adj in final:
            if final[llave] in final[adj]: 
                dirigido = True

print(dirigido)
         
    
        
        
        
 

#print(z)
