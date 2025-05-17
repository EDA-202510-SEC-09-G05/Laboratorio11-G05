from DataStructures.List import array_list as lt
from DataStructures.Priority_queue import index_pq_entry as pq

def new_heap (is_min_pq = True):
    
    queue = {
        'elements': lt.new_list(),
        'size': 0,
        'cmp_function': default_compare_lower_value if is_min_pq else default_compare_higher_value
    }
   
    lt.add_last(queue['elements'], None)
    return queue

def default_compare_lower_value (father_node, child_node):
    
    f = pq.get_key(father_node) 
    
    c = pq.get_key(child_node)
    
    if f <= c:
        return True
    else:
        return False


def default_compare_higher_value (father_node, child_node):
    
    f = pq.get_key(father_node) 
    
    c = pq.get_key(child_node)

    if f >= c:
        return True
    else:
        return False
    

def priority (my_heap, parent, child):
    
    cmp_function = my_heap['cmp_function']
    
    if cmp_function == default_compare_lower_value:
        return cmp_function(parent, child)
    else:
        return cmp_function(child, parent)
    
def insert (my_heap, value, key):
    
    # Añadimos el nuevo elemento al final de la lista
    lt.add_last(my_heap['elements'], pq.new_pq_entry(key, value))
    
    # Aumentamos el tamaño del heap
    my_heap['size'] += 1
    
    # Llamamos a swim para restaurar la propiedad de heap
    swim(my_heap, my_heap['size'])
    
    return my_heap


def swim(my_heap: dict, pos: int):
    """
    Sube el elemento en 'pos' hasta restaurar la propiedad del heap,
    usando priority() y sin break.
    """
    elems = my_heap['elements']
    # Mientras no estemos en la raíz y el padre NO mantenga la prioridad:
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
    
    return my_heap['size']

def is_empty (my_heap):
    
    if my_heap['size'] == 0:
        return True 
    else:
        return False
    
def get_first_priority (my_heap):
    
    cmp_function = my_heap['cmp_function']
    
    if my_heap['size'] > 0:
        if cmp_function == default_compare_lower_value:
            a = my_heap['elements']['elements']
            return a[1]['index']
        else:
            a = my_heap['elements']['elements']
            return a[my_heap['size']]['index']
        
        

def remove (my_heap):

    if my_heap['size'] > 0:
        # guardamos el primer elemento
        a = lt.get_element(my_heap['elements'], 1)
        first = a['index']
    
        # intercambiamos el primero con el último
        lt.exchange(my_heap['elements'], 1, my_heap['size'])
    
        # eliminamos el último (que es el primero)
        lt.remove_last(my_heap['elements'])
    
        # disminuimos el tamaño del heap
        my_heap['size'] -= 1
    
        # restauramos la propiedad de heap
        sink(my_heap, 1)
    else: 
        first = None

    
    return first

def sink(my_heap: dict, pos: int):
    
    elems = my_heap['elements']
    size  = my_heap['size']

    # índice del hijo izquierdo
    left = 2 * pos

    # mientras haya al menos hijo izquierdo
    while left <= size:
        right = left + 1

        # elegimos el hijo favorito: aquel que el padre debe comparar primero
        # (para min-heap: el menor; para max-heap: el mayor)
        if right <= size and not priority(
            my_heap,
            lt.get_element(elems, left),   # tratamos hijo izq como "padre"
            lt.get_element(elems, right)   # y derecho como "hijo"
        ):
            fav = right
        else:
            fav = left

        # si el nodo en pos ya mantiene prioridad frente a fav,
        # forzamos la salida ajustando left por fuera de rango
        if priority(
            my_heap,
            lt.get_element(elems, pos),     # padre
            lt.get_element(elems, fav)      # hijo favorito
        ):
            left = size + 1
        else:
            # si no la mantiene, intercambiamos y seguimos bajando
            lt.exchange(elems, pos, fav)
            pos  = fav
            left = 2 * pos

   