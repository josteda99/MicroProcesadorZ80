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
            flags[1] = flags[4] = '0'
            flags[0] = '1' if len(w) > 0 else '0'
            flags[7] = '1' if str_sum[0] == '1' else '0' 
            flags[6] = '0' if suma != self.__ZERO else '1' 
            flags[2] = '1' if (a & self.__SIGN_BIT) == (b & self.__SIGN_BIT) and ((suma & self.__SIGN_BIT) != (a & self.__SIGN_BIT)) else '0'
        return suma

    def sub(self, a, b, flags):
        with warnings.catch_warnings(record=True) as w:
            subt = a - b
            str_sub = np.binary_repr(subt, 8)
            flags[1] = flags[4] = '1'
            flags[0] = '1' if len(w) > 0 else '0'
            flags[7] = '1' if str_sub[0] == '1' else '0'
            flags[6] = '0' if subt != self.__ZERO else '1'
            flags[2] = '1' if(a & self.__SIGN_BIT) != (b & self.__SIGN_BIT) else '0'
        return subt

    def and_logic(self ,a, b, flags):
        result = a & b
        flags[0] = '0'
        flags[1] = flags[4] = '0'
        flags[7] = '1' if result < 0 else '0'
        flags[6] = '0' if result != self.__ZERO else '1'
        return result

    def or_logic(self, a, b, flags):
        result = a or b
        flags[0] = '0'
        flags[1] = flags[4] = '1'
        flags[7] = '1' if result < 0 else '0'
        flags[6] = '0' if result != self.__ZERO else '1'
        return result

    def xor_logic(self, a, b, flags):
        result = a ^ b
        flags[0] = '0'
        flags[1] = flags[4] = '1'
        flags[7] = '1' if result < 0 else '0'
        flags[6] = '0' if result != self.__ZERO else '1'
        return result

    def increment(self, a, flags):
        result = a + 1
        flags[1] = flags[4] = '1'
        flags[7] = '1' if result < 0 else '0'
        flags[6] = '0' if result != self.__ZERO else '1'
        return result

    def decrement(self, a, flags):
        result = a - 1
        flags[1] = flags[4] = '1'
        flags[7] = '1' if result < 0 else '0'
        flags[6] = '0' if result != self.__ZERO else '1'
        return result

class Register(object):
    
    """
        El tipo de dato de los bits es un String
    """

    def __init__(self, bits):
        self.rgt = ['0' for _ in range(bits)]

    def get_register(self):
        return self.rgt

    def cast_hex(self):
        bit_str = "".join(self.rgt)
        return hex(int (bit_str, 2))

    def cast_int8(self):
        return np.int8("".join(self.rgt))

    def copy_from_array(self, new_register):
        self.rgt = new_register[:]

    def copy_from_int8(self, int_rgs):
        self.rgt = np.binary_repr(int_rgs, 8)

class Memory(object):
    """
        Esta es la memoria RAM
        El directorio de las memoria debe ser de la siguiente manera de
        el indici un string y el valor almacenado un int en formato hex 
    """
    celds = {}
    def __int__(self):
        super(Memory, self).__int__()

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
        self.IR = Register(16)        # Es el que almacena la instrcucion a buscar
        self.SP = Register(16)
        self.PC = Register(16)     # []
        self.alu = ALU

    def fetch(self, memory):
        """
            memory is type Memory
        """
        # empty no sirve para nada pero no la borren xd
        empty = [0 for _ in range(8)]
        self.IR.copy_from_int8(memory.celds[self.PC.cast_hex()])
        new_r = self.alu.increment(self.alu, self.PC.cast_int8(), empty)
        self.PC.copy_from_int8(new_r)

    def decode(self):
        print('No support yet')
