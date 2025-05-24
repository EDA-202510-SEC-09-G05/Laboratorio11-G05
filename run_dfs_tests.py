# run_dfs_tests.py (FINAL VERSION - Copy Entire Content)


# Import graph implementation for tests.
from DataStructures.Graph import no_digraph as g 

from DataStructures.List import array_list as lt # Use array_list, consistent with graph/map
from DataStructures.Stack import stack as stk
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import single_linked_list as sll

# Import your DFS functions
from DataStructures.Graph import dfs as dfs

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
c = g.add_edge(a,'Pablo','Martin', 100)
c = g.add_edge(a,'Pablo','Botanitas', 70)
c = g.add_edge(a,'Pablo','Tommy', 20)
c = g.add_edge(a,'Martin','Sefair', 20)
c = g.add_edge(a,'Tommy','Sefair', 100)
c = g.add_edge(a,'Tommy','Botanitas', 10)


d = dfs.dfs(c,'Pablo')
e = dfs.hasPathTo(d,"Botanitas")
f = dfs.pathTo(d,"Sefair")

x = stk.new_stack()
y = stk.push(x,'Tommy')
y = stk.push(x,'Pablo')
y = stk.push(x,'Martin')


print(f)





