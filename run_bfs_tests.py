
from DataStructures.Graph import no_digraph as g
from DataStructures.Graph import bfs 


a = g.new_graph(5)
b = g.insert_vertex(a, 'Pablo', {'altura': 1.80,
                                 'Musica': 'house'})
b = g.insert_vertex(a, 'Martin', {'altura': 1.70,
                                 'Musica': 'Reggaeton'})
b = g.insert_vertex(a, 'Tommy', {'altura': 1.72,
                                 'Musica': 'Salsa'})
b = g.insert_vertex(a, 'Botanitas', {'altura': 1.90,
                                 'Musica': 'Corroncho'})
b = g.insert_vertex(a, 'Sefair', {'altura': 1.74,
                                 'Musica': 'Rock'})
b = g.insert_vertex(a, 'Soto', {'altura': 1.71,
                                 'Musica': 'Morat'})

c = g.add_edge(a,'Pablo','Martin', 100)
c = g.add_edge(a,'Pablo','Botanitas', 70)
c = g.add_edge(a,'Pablo','Tommy', 20)
c = g.add_edge(a,'Martin','Sefair', 20)
c = g.add_edge(a,'Tommy','Sefair', 100)
c = g.add_edge(a,'Tommy','Botanitas', 10)
c = g.add_edge(a, 'Sefair', 'Soto', 1)



d = bfs.bfs(c,"Pablo")
e = bfs.hasPathTo(d,'Botanitas')
f = bfs.distTo(d,"Soto")
h = bfs.pathTo(d,'Soto')

print(h)