from DataStructures.List import single_linked_list as lt

def new_stack():
    my_stack = {"first": None,
                "last": None,
                "size": 0
                }
    return my_stack



def push(my_stack, element):
    lt.add_last(my_stack,element)
    return my_stack 


def pop(my_stack):
    a = lt.remove_last(my_stack)
    return a

def is_empty(my_stack):
    vacio = False
    if my_stack['size'] == 0:
        vacio = True 
    return vacio 

def top(my_stack):
    if my_stack['size'] == 0:
        raise Exception('EmptyStructureError: stack is empty')
    else:
        node = my_stack['first']
        while node['next'] != None:
            node = node['next']
        
        return node['info']
    
def size(my_stack):
    return my_stack['size']