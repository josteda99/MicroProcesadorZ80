class ALU(object):
    
    __ZERO = bin(0)
    __SIGN_BIT = 1 << 7

    def __init__(self):
        super(ALU, self).__init__()

    def add(self, a, b, flags):
        # Vamos a recibir los valores en '1010101'
        suma = a + b
        suma_separada = str(bin(suma)).split('b')
        flags[0] = 1 if len(suma_separada[1]) > 8 else 0 
        flags[1] = 1
        flags[6] = 0 if suma != self.__ZERO else 1
        flags[7] = 1 if suma_separada[1][3] == 1 else 0
        flags[2] = 1 if (a & self.__SIGN_BIT) == (b & self.__SIGN_BIT) and ((suma & self.__SIGN_BIT) & (a & self.__SIGN_BIT)) else 0
        return suma

    def sub(self, a, b, flags):
        resta = a - b
        resta_separada = str(resta).split('b')
        # if(resta_separada[1].len > 8):
        return resta

    def and_logic(self ,a, b, flags):
        result = a and b
        print(result)
        return result

    def or_logic(self, a, b, flags):
        result = a or b
        # print(result)
        return result


    def xor_logic(self, a, b, flags):
        result = bool(a) != bool(b)
        return result


    def compare(self, a, b):
        # Funcion que rotornaria las banderas respctivas para la operacion echa
        
        # if(a - b == 0):
        #     # a es igual b 
        # elif(a - b < 0):
        #     # a es menor que b
        # elif(a - b > 0 ):
        #     # a es mayor que b
        
        # return 
        print("Not supported yet")

    def lr_bit_switch(self, a, is_left, flags):
        if(is_left):
            result  = a << 1
        else:
            result = a >> 1
        return result 

    def increment(self, a, flags):
        result = a + 1
        return result

    def decrement(self, a, flags):
        result = a - 1
        return result

class Register(object):
    def __init__(self, bits):
        self.len = bits
        self.register = []
        
    def get_register(self):
        print("a")
    # def register():
        
    # def write():
    

class Memory(object):
    
    grid_memory = [] # si esuna 
    
    def __init__(self, *args):
        super(Memory, self).__init__(*args)
        