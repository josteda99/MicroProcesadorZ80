import numpy as np
import warnings
warnings.simplefilter("always")

class ALU(object):
    
    __ZERO = 0
    __SIGN_BIT = 1 << 7

    def __init__(self):
        super(ALU, self).__init__()

    def add(self, a, b, flags):
        # Los valores son de tipo int8 de numpy
        suma = 0
        with warnings.catch_warnings(record=True,) as w:
            suma = a + b
            str_sum = np.binary_repr(suma, 8)
            flags[1] = flags[4] = 0
            flags[0] = 1 if len(w) > 0 else 0
            flags[7] = 1 if str_sum[0] == '1' else 0 
            flags[6] = 0 if suma != self.__ZERO else 1 
            flags[2] = 1 if (a & self.__SIGN_BIT) == (b & self.__SIGN_BIT) and ((suma & self.__SIGN_BIT) != (a & self.__SIGN_BIT)) else 0
        return suma

    def sub(self, a, b, flags):
        with warnings.catch_warnings(record=True) as w:
            subt = a - b
            str_sub = np.binary_repr(subt, 8)
            flags[1] = flags[4] = 1
            flags[0] = 1 if len(w) > 0 else 0
            flags[7] = 1 if str_sub[0] == '1' else 0
            flags[6] = 0 if subt != self.__ZERO else 1
            flags[2] = 1 if(a & self.__SIGN_BIT) != (b & self.__SIGN_BIT) else 0
        return subt

    def and_logic(self ,a, b, flags):
        result = a & b
        flags[0] = 0
        flags[1] = flags[4] = 1
        flags[7] = 1 if result[0] == '1' else 0
        flags[6] = 0 if result != self.__ZERO else 1
        return result

    def or_logic(self, a, b, flags):
        result = a or b
        flags[0] = 0
        flags[1] = flags[4] = 1
        flags[7] = 1 if result[0] == '1' else 0
        flags[6] = 0 if result != self.__ZERO else 1
        return result


    def xor_logic(self, a, b, flags):
        result = a ^ b
        flags[0] = 0
        flags[1] = flags[4] = 1
        flags[7] = 1 if result[0] == '1' else 0
        flags[6] = 0 if result != self.__ZERO else 1
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
        self.rgt = []
        
    def get_register(self):
        return self.rgt

class Memory(object):
    
    grid_memory = [] # si esuna 
    
    def __init__(self, *args):
        super(Memory, self).__init__(*args)
        