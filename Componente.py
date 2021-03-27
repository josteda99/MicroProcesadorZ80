import numpy as np
import warnings
warnings.simplefilter("always")

class ALU(object):

    __ZERO = 0
    __SIGN_BIT = 1 << 7
    __instance = None

    def __init__(self):
        if ALU.__instance is None:
            ALU.__instance = self

    def add(self, a, b, flags):
        # Los valores son de tipo int8 de numpy
        with warnings.catch_warnings(record=True) as w:
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
        flags[1] = flags[4] = 0
        flags[7] = 1 if result < 0 else 0
        flags[6] = 0 if result != self.__ZERO else 1
        return result

    def or_logic(self, a, b, flags):
        result = a or b
        flags[0] = 0
        flags[1] = flags[4] = 1
        flags[7] = 1 if result < 0 else 0
        flags[6] = 0 if result != self.__ZERO else 1
        return result

    def xor_logic(self, a, b, flags):
        result = a ^ b
        flags[0] = 0
        flags[1] = flags[4] = 1
        flags[7] = 1 if result < 0 else 0
        flags[6] = 0 if result != self.__ZERO else 1
        return result

    def increment(self, a, flags):
        result = a + 1
        flags[1] = flags[4] = 1
        flags[7] = 1 if result < 0 else 0
        flags[6] = 0 if result != self.__ZERO else 1
        return result

    def decrement(self, a, flags):
        result = a - 1
        flags[1] = flags[4] = 1
        flags[7] = 1 if result < 0 else 0
        flags[6] = 0 if result != self.__ZERO else 1
        return result

class Register(object):

    def __init__(self, bits):
        self.rgt = [0 for _ in range(bits)]

    def get_register(self):
        return self.rgt

    def cast_hex(self):
        print('No support yet')

    def cast_int8():
        print('No support yet')

class Memory(object): 
    # Esta es la RAM y ROM
    __instance = None
    celds = {}
    def __int__(self, *args):
        if Memory.__instance is None:
            Memory.__instance = self

class Processor(object):

    def __init__(self, *args):
        super(Processor, self).__init__(*args)
        self.A = Register(8)        # Acumulador
        self.B = Register(8)
        self.C = Register(8)
        self.D = Register(8)
        self.F = Register(8)        # flags
        self.H = Register(8)
        self.L = Register(8)
        self.IR = Register(8)        # Es el que almacena la instrcucion a buscar
        self.IX = Register(16)
        self.IY = Register(16)
        self.SP = Register(16)
        self.PC = Register(16)     # []
        self.alu = ALU

    def fectch(self):
        halt = False;
        while halt == False:
            with switch(bits(ir,15,12)) as s: # definir como se ingresa
                if s.case(''):

                
        
    #def decode(self):
