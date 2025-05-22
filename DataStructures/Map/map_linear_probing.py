from DataStructures.Map import map_functions as mp
import random as rd
from DataStructures.List import array_list as lt
from DataStructures.Map import map_entry as me


def new_map(num_elements,load_factor, prime=109345121):
    capacity = mp.next_prime(num_elements//load_factor)
    scale = rd.randint(1,prime -1)
    shift = rd.randint(0, prime -1)
    hash_table = {'prime': prime,
                  "capacity": capacity,
                  "scale": scale,
                  "shift": shift,
                  "table": lt.new_list(),
                  "current_factor": 0,
                  "limit_factor": load_factor,
                  'size': 0,
                  'type': 'PROBE_HASH_MAP'} # LINEAR PROBBING. 
    
    for i in range(capacity):
        entry = me.new_map_entry(None,None)
        lt.add_last(hash_table['table'], entry)
    hash_table['scale'] = 1
    hash_table['shift'] = 0
    
        
    return hash_table

def put(my_map, key, value):
    #Paso 1: Calcular el hash, de la llave usando la funcion hash_value
    hash = mp.hash_value(my_map, key)
    #Paso 2: Se busca la posicion donde ingresar. 
    pos_fake = find_slot(my_map, key, hash)
    
    if pos_fake[0] != True:
            pos = pos_fake[1]
            #Paso 3: Se inserta la entrada en la tabla Si la posicion no esta ocupada.
            my_map['table']['elements'][pos] = me.new_map_entry(key, value)
            my_map['size'] += 1 # se inserto una nueva llave, valor
    else:
        pos = pos_fake[1]
        #Paso 3: Se inserta la entrada en la tabla Si la posicion no esta ocupada.
        my_map['table']['elements'][pos] = me.new_map_entry(key, value)
        
    
    #Paso 4: Actualizar el current factor.
    my_map['current_factor'] = my_map['size'] / my_map['capacity']
    
    if my_map['current_factor'] > my_map["limit_factor"]:
        my_map = rehash(my_map)

    # Paso 5: Actualizar el size de la lista
   
    #Paso 6: retornar
    return my_map

def find_slot(my_map, key, hash_value):
   first_avail = None
   found = False
   ocupied = False
   while not found:
      if is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = lt.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif default_compare(key, lt.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail

def is_available(table,pos):
   entry = lt.get_element(table, pos)
   if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
      return True
   return False

def default_compare(key,entry):
    if key == me.get_key(entry):
      return 0
    elif key > me.get_key(entry):
      return 1
    return -1

def contains(my_map, key): # SE puede mejorar con binary_SEARCH. 
    for i in range(my_map['table']['size']):
        if key == my_map["table"]['elements'][i]['key']:
            return True
    return False

def get(my_map, key):
    hash_value = mp.hash_value(my_map, key)
    capacity = my_map["capacity"]
    initial_pos = hash_value
    checked_slots = 0
    
    while checked_slots < capacity:
        entry = lt.get_element(my_map["table"], hash_value)
        
        # Caso 1: Encontramos la clave
        if me.get_key(entry) == key:
            return me.get_value(entry)
        
        # Caso 2: Slot vacío (clave no existe)
        if me.get_key(entry) is None:
            return None
            
        # Linear probing: siguiente slot
        hash_value = (hash_value + 1) % capacity
        checked_slots += 1
        
        # Optimización: si volvemos al inicio sin encontrar, salir
        if hash_value == initial_pos:
            return None
        
        
    
def remove(my_map, key):
    posicion = 0 
    for i in range(my_map['table']['size']):
        if key == my_map['table']['elements'][i]['key']:
            posicion = i
            break
    nueva_lista = lt.new_list()
    for i in range(0,posicion - 1):
        lt.add_last(nueva_lista, my_map['table']['elements'][i])
        
    for i in range(posicion + 1, my_map['table']['size']):
        lt.add_last(nueva_lista,my_map['table']['elements'][i])
    
    my_map['table'] = nueva_lista
    my_map['size'] -= 1
    
    return my_map
    
def size(my_map):
    return my_map['size']

        
def is_empty(my_map):
    return my_map["size"] == 0

def key_set(my_map):
    keys = lt.new_list()
    
    for i in range(len(my_map["table"]["elements"])):
        if my_map["table"]["elements"][i] is not None and my_map['table']["elements"][i]['key'] is not None and my_map['table']["elements"][i]['key'] != -1:
            lt.add_last(keys, my_map['table']['elements'][i]['key'])
    
    
    return keys

def value_set(my_map):
    values = lt.new_list()
    for i in range(len(my_map["table"]["elements"])):
        if my_map["table"]["elements"][i] is not None and my_map["table"]["elements"][i]["key"] is not None and my_map["table"]["elements"][i]["key"] != -1:
            lt.add_last(values, my_map["table"]["elements"][i]["value"])
            
    return values
    


def rehash(my_map): 
    num_elements = mp.next_prime(2 * my_map['capacity'])
    #Paso 1: Crear una nueva tabla, modo linear probbing con capacity que sea el siguiente primo al doble del capacity actual.
    nuevo = new_map(num_elements, 0.5) 
    nuevo['size'] = my_map['size']
    #Paso 2: Insertar los datos de la tabla vieja en la nueva tabla
    llaves = key_set(my_map)
    for key in llaves['elements']:
        value = get(my_map, key)
        put(nuevo, key, value)
    nuevo['current_factor'] = nuevo['size'] / nuevo['capacity']
    
    return nuevo
    
    
 #PRueba, no sirve para nada la funcion de abajo solo probando ando.    
\
            