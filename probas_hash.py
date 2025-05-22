from DataStructures.Map import map_functions as mp
import random as rd
from DataStructures.List import array_list as lt
from DataStructures.Map import map_entry as me

# --- Internal Helper Function (NEW) ---
# Esta función realiza la inserción o actualización sin disparar un rehash.
# Es llamada por 'put' y 'rehash'.
def _put_internal(my_map, key, value):
    hash_val = mp.hash_value(my_map, key)
    
    # 'find_slot' ahora devuelve si la clave fue encontrada y la posición.
    key_already_exists, pos = find_slot(my_map, key, hash_val)

    if not key_already_exists:
        # Es una nueva inserción
        my_map['table']['elements'][pos] = me.new_map_entry(key, value)
        my_map['size'] += 1 # Incrementar el tamaño solo para nuevas claves
    else:
        # La clave ya existe, solo actualizamos su valor
        my_map['table']['elements'][pos] = me.new_map_entry(key, value)

# --- new_map function (Corregida) ---
def new_map(num_elements, load_factor, prime=109345121):
    # Calcula la capacidad inicial como el siguiente primo más grande
    # que el número de elementos esperados dividido por el factor de carga.
    # Esto asegura que la tabla inicie con un tamaño adecuado.
    capacity = mp.next_prime(int(num_elements / load_factor)) # Usar int para la división entera
    scale = rd.randint(1, prime - 1)
    shift = rd.randint(0, prime - 1)
    
    hash_table = {
        'prime': prime,
        "capacity": capacity,
        "scale": scale,
        "shift": shift,
        "table": lt.new_list(), # Inicializa la estructura del array_list
        "current_factor": 0,
        "limit_factor": load_factor,
        'size': 0, # El tamaño inicial de elementos en el mapa
        'type': 'PROBE_HASH_MAP'
    }
    
    # OPTIMIZACIÓN: Inicializar directamente la lista interna del array_list.
    # Esto evita el comportamiento O(N^2) si lt.add_last es ineficiente por reasignaciones.
    # Asume que 'lt.new_list()' retorna un diccionario con la clave 'elements'.
    hash_table['table']['elements'] = [me.new_map_entry(None, None) for _ in range(capacity)]
    hash_table['table']['size'] = capacity # Actualiza el tamaño de la lista interna del array_list
    
    # Los valores de 'scale' y 'shift' no deberían ser reiniciados a 1 y 0
    # si se usan para la función de hash universal. Los mantendremos aleatorios.
    # hash_table['scale'] = 1
    # hash_table['shift'] = 0
    
    return hash_table

# --- put function (Corregida) ---
def put(my_map, key, value):
    # Utilizamos la función auxiliar interna para manejar la lógica de inserción/actualización.
    _put_internal(my_map, key, value)
    
    # Paso 4: Actualizar el current factor.
    my_map['current_factor'] = my_map['size'] / my_map['capacity']
    
    # Paso 5: Verificar si es necesario hacer un rehash (solo después de la inserción).
    if my_map['current_factor'] > my_map["limit_factor"]:
        my_map = rehash(my_map) # 'rehash' devuelve un nuevo mapa.
    
    return my_map

# --- find_slot function (Corregida) ---
def find_slot(my_map, key, hash_value):
   first_avail = None # Almacena la primera ranura disponible (None o "__EMPTY__")
   current_pos = hash_value # Posición actual en la búsqueda
   probes = 0 # Contador para evitar bucles infinitos en tablas llenas

   while probes < my_map["capacity"]: # Limita la búsqueda a la capacidad total de la tabla
      entry = lt.get_element(my_map["table"], current_pos)
      
      # Caso 1: Encontramos la clave buscada
      if me.get_key(entry) == key:
            return True, current_pos # Retorna (clave_encontrada=True, posicion_de_la_clave)
      
      # Caso 2: Ranura vacía (clave None)
      if me.get_key(entry) is None:
            if first_avail is None:
               first_avail = current_pos # Esta es la mejor posición para insertar si la clave no se encuentra
            # Si encontramos un None y la clave no ha sido encontrada,
            # significa que la clave no está en la tabla (no hay más sondeo necesario para la búsqueda).
            return False, first_avail # Retorna (clave_encontrada=False, mejor_posicion_para_insertar)
      
      # Caso 3: Ranura marcada como vacía por borrado ("__EMPTY__" / tumba)
      if me.get_key(entry) == "__EMPTY__":
            if first_avail is None:
               first_avail = current_pos # Esta ranura es utilizable para una nueva inserción
            # Continuamos sondeando, porque la clave podría estar más adelante
            # en la secuencia de sondeo (debido a colisiones previas).
      
      # Mover a la siguiente ranura en la secuencia de sondeo lineal
      current_pos = (current_pos + 1) % my_map["capacity"]
      probes += 1 # Incrementar el contador de sondeos
      
   # Si el bucle termina, significa que hemos sondeado toda la tabla (o la tabla está llena).
   # Si no se encontró la clave, devolvemos 'False' y la primera ranura disponible encontrada (si hubo).
   # Si 'first_avail' sigue siendo None, la tabla está completamente llena sin ranuras disponibles.
   return False, first_avail if first_avail is not None else -1 # -1 podría indicar tabla llena o sin slot disponible

# --- is_available function (Se mantiene igual, funciona bien) ---
def is_available(table, pos):
   entry = lt.get_element(table, pos)
   if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
      return True
   return False

# --- default_compare function (Se mantiene igual, funciona bien) ---
def default_compare(key, entry):
    # Asume que entry es el objeto devuelto por me.new_map_entry
    entry_key = me.get_key(entry)
    if key == entry_key:
      return 0
    elif key > entry_key: # Asume que las claves son comparables
      return 1
    return -1

# --- contains function (Corregida para usar get) ---
def contains(my_map, key):
    # Utiliza la función 'get' para verificar si la clave existe.
    return get(my_map, key) is not None

# --- get function (Corregida con un ligero ajuste) ---
def get(my_map, key):
    hash_value = mp.hash_value(my_map, key)
    capacity = my_map["capacity"]
    current_pos = hash_value # Usar una variable para la posición actual
    probes = 0 # Contador para evitar bucles infinitos
    
    while probes < capacity: # Limitar la búsqueda a la capacidad total
        entry = lt.get_element(my_map["table"], current_pos)
        
        # Caso 1: Encontramos la clave
        if me.get_key(entry) == key:
            return me.get_value(entry)
        
        # Caso 2: Ranura vacía (clave None)
        # Si encontramos un slot None, la clave no puede estar más adelante en esta secuencia.
        if me.get_key(entry) is None:
            return None
            
        # Caso 3: Ranura es una tumba ("__EMPTY__")
        # Continuamos sondeando, porque la clave podría estar más adelante.
        # No necesitamos un 'elif' explícito aquí, el flujo continúa si no es None o la clave.
        
        # Linear probing: siguiente slot
        current_pos = (current_pos + 1) % capacity
        probes += 1
        
    # Si salimos del bucle, significa que la clave no se encontró después de sondear toda la tabla.
    return None
    
# --- remove function (Corregida con Lazy Deletion/Tombstones) ---
def remove(my_map, key):
    # Utiliza la lógica de sondeo para encontrar la clave.
    # No podemos usar 'find_slot' directamente porque necesitamos la posición de la clave, no una de inserción.
    
    hash_value = mp.hash_value(my_map, key)
    current_pos = hash_value
    probes = 0
    
    while probes < my_map["capacity"]:
        entry = lt.get_element(my_map["table"], current_pos)
        
        if me.get_key(entry) == key:
            # Clave encontrada: Marcar como eliminada (tumba)
            my_map['table']['elements'][current_pos] = me.new_map_entry("__EMPTY__", None)
            my_map['size'] -= 1 # Decrementar el tamaño del mapa
            return my_map
        
        if me.get_key(entry) is None:
            # Encontramos un slot None, la clave no está en la tabla
            return my_map # La clave no existe en el mapa
            
        current_pos = (current_pos + 1) % my_map["capacity"]
        probes += 1
        
    return my_map # Clave no encontrada después de sondear toda la tabla

# --- size function (Se mantiene igual, funciona bien) ---
def size(my_map):
    return my_map['size']

# --- is_empty function (Se mantiene igual, funciona bien) ---
def is_empty(my_map):
    return my_map["size"] == 0

# --- key_set function (Corregida ligeramente para robustez) ---
def key_set(my_map):
    keys = lt.new_list()
    # Iterar sobre toda la capacidad de la tabla para encontrar todas las claves
    for i in range(my_map["capacity"]): # Iterar hasta la capacidad
        current_entry = my_map["table"]["elements"][i]
        # Asegurarse de que la entrada no es None ni una tumba
        if current_entry is not None and me.get_key(current_entry) is not None and me.get_key(current_entry) != "__EMPTY__":
            lt.add_last(keys, me.get_key(current_entry))
    return keys

# --- value_set function (Corregida ligeramente para robustez) ---
def value_set(my_map):
    values = lt.new_list()
    # Iterar sobre toda la capacidad de la tabla para encontrar todos los valores
    for i in range(my_map["capacity"]): # Iterar hasta la capacidad
        current_entry = my_map["table"]["elements"][i]
        # Asegurarse de que la entrada no es None ni una tumba
        if current_entry is not None and me.get_key(current_entry) is not None and me.get_key(current_entry) != "__EMPTY__":
            lt.add_last(values, me.get_value(current_entry))
    return values

# --- rehash function (Corregida) ---
def rehash(my_map):
    # Calcula la nueva capacidad (doble de la actual, y el siguiente primo)
    new_capacity_val = mp.next_prime(2 * my_map['capacity'])
    
    # Crea un nuevo mapa con la nueva capacidad calculada.
    # 'new_map' calculará la capacidad real basada en 'new_capacity_val' y el factor de carga.
    nuevo = new_map(new_capacity_val, my_map['limit_factor'])
    
    # El tamaño del nuevo mapa se construirá correctamente a medida que insertamos.
    # NO: nuevo['size'] = my_map['size'] # Esto era un error.

    # Inserta todos los elementos de la tabla vieja en la nueva tabla
    # Iterar sobre la tabla antigua para encontrar elementos válidos (no None ni tumbas)
    for i in range(my_map['capacity']):
        entry = lt.get_element(my_map['table'], i)
        if entry is not None and me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
            key = me.get_key(entry)
            value = me.get_value(entry)
            _put_internal(nuevo, key, value) # Usar la función interna para no disparar otro rehash

    # El current_factor del nuevo mapa se actualizará automáticamente con cada _put_internal
    # o puede ser recalculado aquí una vez que todos los elementos han sido transferidos.
    # nuevo['current_factor'] = nuevo['size'] / nuevo['capacity'] # Ya se calcula en _put_internal

    return nuevo



lista = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,]
a = new_map(10,0.5)

for i in lista:
    put(a,i,"joda")
    
    
print(a)