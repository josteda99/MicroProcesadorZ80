class ALU(object):

    def __init__(self):
        super(ALU, self).__init__()

    def add(a, b, flags):
        # Vamos a recibir los valores en '1010101'
        suma = a + b
        suma_separada = str(suma).split('b')
        if suma_separada[1].len > 8:
            print("Not supported yet")
            # flags = 
        return suma

    def sub(a, b, flags):
        print("Not supported yet")

    def and_logic(a, b, flags):
        print("Not supported yet")

    def or_logic(a, b, flags):
        print("Not supported yet")

    def xor_logic(a, b, flags):
        print("Not supported yet")

    def compare(a, b):
        # Funcion que rotornaria las banderas respctivas para la operacion echa
        print("Not supported yet")

    def lr_bit_switch(a, b):
        print("Not supported yet")

    def increment(a):
        print("Not supported yet")

    def decrement(a):
        print("Not supported yet")

class Register(object):
    def __init__(self, *args):
        super(Register, self).__init__(*args)

class Memory(object):
    
    grid_memory = [] # si esuna 

    def __init__(self, *args):
        super(Memory, self).__init__(*args)
        