from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Priority_queue import priority_queue as pq
import math # Not strictly needed here, but good practice for numerical ops

def new_dijsktra_structure(source_key, g_order):
    """
    Crea una estructura de búsqueda usada en el algoritmo **Dijkstra**.

    Se crea una estructura de búsqueda con los siguientes atributos:

    - **source**: Vértice de origen. Se inicializa en `source_key`.
    - **dist_to**: Mapa que almacena la distancia más corta conocida desde el origen a cada vértice.
    - **edge_to**: Mapa que almacena el vértice predecesor en el camino más corto conocido.
    - **marked**: Mapa booleano que indica si un vértice ya ha sido procesado/finalizado.
    - **pq**: Cola de prioridad para extraer eficientemente el vértice no marcado con la menor distancia.

    :param source_key: La clave del vértice de origen para esta búsqueda.
    :param g_order: El número total de vértices en el grafo, usado para la inicialización de mapas.
    :returns: Un diccionario que representa la estructura de búsqueda de Dijkstra.
    :rtype: dict
    """

    structure = {
        "source": source_key,
        "dist_to": map.new_map(num_elements=g_order, load_factor=0.5), 
        "edge_to": map.new_map(num_elements=g_order, load_factor=0.5), 
        "marked": map.new_map(num_elements=g_order, load_factor=0.5), 
        "pq": pq.new_heap(is_min_pq=True) 
    }
    
    return structure