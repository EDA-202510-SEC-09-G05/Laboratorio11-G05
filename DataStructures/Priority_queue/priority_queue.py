from DataStructures.List import array_list as lt
from DataStructures.Priority_queue import index_pq_entry as pq 

def new_heap (is_min_pq = True):
    """
    Crea una nueva estructura de heap (cola de prioridad).
    :param is_min_pq: True para un min-heap (menor prioridad primero), False para un max-heap.
    :returns: Un diccionario que representa el heap.
    """
    queue = {
        'elements': lt.new_list(),
        'size': 0,
        'cmp_function': default_compare_lower_value if is_min_pq else default_compare_higher_value
    }
   
    # El índice 0 se deja vacío en los heaps basados en arrays para simplificar cálculos de padres/hijos.
    lt.add_last(queue['elements'], None) 
    return queue

def default_compare_lower_value (father_node, child_node):
    """
    Función de comparación para un min-heap.
    Retorna True si el padre tiene menor o igual prioridad que el hijo.
    """
    f = pq.get_key(father_node) # Asume que pq.get_key obtiene la prioridad
    c = pq.get_key(child_node)
    
    if f <= c:
        return True
    else:
        return False


def default_compare_higher_value (father_node, child_node):
    """
    Función de comparación para un max-heap.
    Retorna True si el padre tiene mayor o igual prioridad que el hijo.
    """
    f = pq.get_key(father_node) # Asume que pq.get_key obtiene la prioridad
    c = pq.get_key(child_node)

    if f >= c:
        return True
    else:
        return False
    

def priority (my_heap, parent, child):
    """
    Compara la prioridad de dos nodos según la función de comparación del heap.
    """
    cmp_function = my_heap['cmp_function']
    
    # Para min-heap, compara padre con hijo. Para max-heap, la función de comparación
    # ya está invertida (mayor >= menor), así que la llamada es directa.
    return cmp_function(parent, child)
    
def put (my_heap, priority_value, item_value): # RENAMED: 'insert' to 'put'
    """
    Inserta un nuevo elemento en el heap con su prioridad.
    :param my_heap: El heap.
    :param priority_value: El valor de prioridad del elemento.
    :param item_value: El elemento a insertar.
    """
    # Añadimos el nuevo elemento al final de la lista
    # pq.new_pq_entry(key, value) -> assuming key is priority, value is item
    lt.add_last(my_heap['elements'], pq.new_pq_entry(priority_value, item_value)) 
    
    # Aumentamos el tamaño del heap
    my_heap['size'] += 1
    
    # Llamamos a swim para restaurar la propiedad de heap
    swim(my_heap, my_heap['size'])
    
    return my_heap


def swim(my_heap: dict, pos: int):
    """
    Sube el elemento en 'pos' hasta restaurar la propiedad del heap.
    """
    elems = my_heap['elements']
    # Mientras no estemos en la raíz (pos > 1) y el padre NO mantenga la prioridad frente al hijo:
    while pos > 1 and not priority(
        my_heap,
        lt.get_element(elems, pos // 2),  # padre
        lt.get_element(elems, pos)         # hijo
    ):
        # intercambiamos padre e hijo
        lt.exchange(elems, pos // 2, pos)
        # subimos un nivel
        pos //= 2

def size (my_heap):
    """
    Retorna el número de elementos en el heap.
    """
    return my_heap['size']

def is_empty (my_heap):
    """
    Verifica si el heap está vacío.
    """
    return my_heap['size'] == 0
    
def get_first_priority (my_heap):
    """
    Retorna la prioridad del primer elemento (raíz) sin eliminarlo.
    """
    if my_heap['size'] > 0:
        # Para min-heap, es la raíz (índice 1). Para max-heap, también es la raíz.
        # Asume que pq.get_key obtiene la prioridad.
        return pq.get_key(lt.get_element(my_heap['elements'], 1))
    return None # Retorna None si el heap está vacío
        
def del_min (my_heap): # RENAMED: 'remove' to 'del_min'
    """
    Elimina y retorna el elemento de mayor prioridad (raíz) del heap.
    :returns: Una tupla (priority_value, item_value) del elemento eliminado.
              Retorna (None, None) si el heap está vacío.
    """
    if my_heap['size'] == 0:
        return None, None # Retorna (None, None) si el heap está vacío

    # Guardamos el primer elemento (raíz)
    first_entry = lt.get_element(my_heap['elements'], 1)
    
    # Extraemos la prioridad y el valor del elemento
    priority_value = pq.get_key(first_entry)   # Asume que pq.get_key obtiene la prioridad
    item_value = pq.get_index(first_entry)     # Asume que pq.get_value obtiene el valor del elemento

    # Intercambiamos el primer elemento con el último
    lt.exchange(my_heap['elements'], 1, my_heap['size'])
    
    # Eliminamos el último elemento (que ahora es el original 'first_entry')
    lt.remove_last(my_heap['elements'])
    
    # Disminuimos el tamaño del heap
    my_heap['size'] -= 1
    
    # Restauramos la propiedad de heap hundiendo el nuevo elemento en la raíz
    if my_heap['size'] > 0: # Solo si quedan elementos
        sink(my_heap, 1)
        
    return (priority_value, item_value) # Retorna la tupla (prioridad, valor)

def sink(my_heap: dict, pos: int):
    """
    Baja el elemento en 'pos' hasta restaurar la propiedad del heap.
    """
    elems = my_heap['elements']
    size  = my_heap['size']

    # Índice del hijo izquierdo
    left = 2 * pos

    # Mientras haya al menos hijo izquierdo
    while left <= size:
        right = left + 1

        # Elegimos el hijo favorito: aquel que el padre debe comparar primero
        # (para min-heap: el menor; para max-heap: el mayor)
        fav = left # Asumimos inicialmente que el hijo izquierdo es el favorito
        if right <= size and not priority( # Si hay hijo derecho y el hijo izquierdo NO tiene prioridad sobre el derecho
            my_heap,
            lt.get_element(elems, left),   # tratamos hijo izq como "padre"
            lt.get_element(elems, right)   # y derecho como "hijo"
        ):
            fav = right # Entonces el hijo derecho es el favorito

        # Si el nodo en pos ya mantiene prioridad frente a su hijo favorito,
        # la propiedad de heap se cumple, salimos del bucle.
        if priority(
            my_heap,
            lt.get_element(elems, pos),     # padre
            lt.get_element(elems, fav)      # hijo favorito
        ):
            break # Salimos del bucle
        else:
            # Si no la mantiene, intercambiamos y seguimos bajando
            lt.exchange(elems, pos, fav)
            pos  = fav
            left = 2 * pos # Actualizamos el índice del hijo izquierdo para la siguiente iteración