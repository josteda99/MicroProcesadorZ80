class ALU(object):

    def __init__(self):
        super(ALU, self).__init__()

    def add(a, b, flags):
        # Vamos a recibir los valores en '1010101'
        suma = a + b
        suma_separada = str(suma).split('b')
        if suma_separada[1].len > 8:
            # flags = 
        return suma

    def sub(a, b, flags):
        
    def and_logic(a, b, flags):
        

    def or_logic(a, b, flags):
        

    def xor_logic(a, b, flags):
        

    def compare(a, b):
        # Funcion que rotornaria las banderas respctivas para la operacion echa

    def left_right_bit_Switch(a, b):
        

    def increment(a):
        

    def decrement(a):
        print("No supported yet")

class Register(object):
    def __init__(self, *args):
        super(Register, self).__init__(*args)

class Memory(object):
    
    grid_memory = [] # si esuna 

    def __init__(self, *args):
        super(Memory, self).__init__(*args)
        