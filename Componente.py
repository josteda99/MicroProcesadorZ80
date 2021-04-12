import warnings

import numpy as np

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

    def cop_one(self, a, flags):
        a = ['0' if bit == '1' else '1' for bit in a]
        flags[4] = flags[1] = '1'
        return a

class Register(object):
    
    """
        El tipo de dato de los bits es un String
    """

    def __init__(self, bits):
        self.bits = bits
        self.rgt = ['0' for _ in range(bits)]

    def get_register(self):
        return self.rgt

    def cast_hex(self):
        bit_str = "".join(self.rgt)
        hex_v = hex(int (bit_str, 2)).upper()
        if len(hex_v) == 5:
            hex_v = "0X0" + hex_v[2:]
        elif len(hex_v) == 4 and self.bits == 16:
            hex_v = "0X00"   + hex_v[2:]
        elif len(hex_v) == 3:
            hex_v = ("0X000" if self.bits == 16 else "0X0") + hex_v[2]
        return hex_v

    def cast_int8(self):
        if self.bits == 8:
            return np.int8(int ("".join(self.rgt), 2))
        else:
            return np.int16(int ("".join(self.rgt), 2))

    def copy_from_array(self, new_register):
        self.rgt = new_register[:]

    def copy_from_int8(self, int_rgs):
        self.rgt = list (np.binary_repr(int_rgs, self.bits))

class Memory(object):
    """
        Esta es la memoria RAM
        El directorio de las memoria debe ser de la siguiente manera de
        el indici un string y el valor almacenado un np.int8 en formato hex 
    """
    def __init__(self, *args):
        super(Memory, self).__init__(*args)
        self.celds = {}

    def get_celds(self):
        return self.celds

class Processor(object):

    def __init__(self, *args):
        super(Processor, self).__init__(*args)
        self.A = Register(8)        # Acumulador
        self.B = Register(8)
        self.C = Register(8)
        self.D = Register(8)
        self.E = Register(8)
        self.F = Register(8)        # flags
        self.H = Register(8)
        self.L = Register(8)
        self.IR = Register(16)        # Es el que almacena la instrcucion a buscar
        self.SP = Register(16)
        self.PC = Register(16)     # []
        self.alu = ALU

    def fetch(self, memory_ram):
        """
            memory is type Memory
        """
        # empty no sirve para nada pero no la borren xd
        empty = [0 for _ in range(8)]
        self.IR.copy_from_int8(memory_ram.get_celds()[self.PC.cast_hex()])
        new_r = self.alu.increment(self.alu, self.PC.cast_int8(), empty)
        self.PC.copy_from_int8(new_r)

    def decode(self, memory_rom, memory_ram, in_byte):
        print('IR: ', self.IR.get_register())
        print('A antes decode: ', self.A.get_register())
        print(self.IR.cast_hex())
        print(self.IR.cast_hex()[:3])
        Processor.__ISA.get(self.IR.cast_hex()[:3])(self, memory_rom, memory_ram, in_byte)
        print('A despues decode: ', self.A.get_register())
        print('F: ', self.F.get_register())

    def __get_value_hl__(self, memory_rom):
        '''
            Retorna el valor que este en la posicion de memoria HL
        '''
        h, l = self.H.cast_hex(), self.L.cast_hex()
        dirc = '0X' + h[2:] + l[2:] if h[2] != '0' and l[2] != '0' else '0X0'
        return memory_rom.get_celds()[dirc]

    def __set_value_hl__(self, hex_value, memory_rom):
        h, l = self.H.cast_hex(), self.L.cast_hex()
        dirc = '0X' + h[2:] + l[2:] if h[2] != '0' and l[2] != '0' else '0X0'
        memory_rom.get_celds()[dirc] = int (hex_value, 16)

    def ze_f(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0X0
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == '0':        # NOP
            pass
        elif ir_hex[3] == '4':      # INC B
            new_reg = self.alu.increment(self.alu, self.B.cast_int8(), self.F.get_register())
            self.B.copy_from_int8(new_reg)
        elif ir_hex[3] == '5':      # DEC B
            new_reg = self.alu.decrement(self.alu, self.B.cast_int8(), self.F.get_register())
            self.B.copy_from_int8(new_reg)
        elif ir_hex[3] == 'C':      # INC C
            new_reg = self.alu.increment(self.alu, self.C.cast_int8(), self.F.get_register())
            self.C.copy_from_int8(new_reg)
        elif ir_hex[3] == 'D':      # DEC C
            new_reg = self.alu.decrement(self.alu, self.C.cast_int8(), self.F.get_register())
            self.C.copy_from_int8(new_reg)
        elif ir_hex[3] == '6':      # LD B, n
            bits = list (bin(int (self.IR.cast_hex()[4:], 16))[2:])
            self.B.copy_from_array(bits)
        elif ir_hex[3] == '7':      #RLCA
            self.F.get_register()[0] = self.A.get_register()[0]#poner el primer elemento del acumulador en carry flag ->
            a = []
            a.extend(self.A.get_register()[1:8])#poner el resto del arreglo de 1 a 7
            a.append(self.F.get_register()[0])#poner en el nuevo valor del acumulador el valor de carry flag
            self.A.copy_from_array(a)#poner ese valor en el acumulador
        elif ir_hex[3] == 'E':      # LD C,n
            bits = list (bin(int (self.IR.cast_hex()[4:], 16))[2:])
            self.C.copy_from_array(bits)
        elif ir_hex[3] == 'A':      # LD A, (BC)
            b, c = self.B.cast_hex(), self.C.cast_hex()
            dirc = '0X' + b[2:] + c[2:] if b[2] != '0' and c[2] != '0' else '0X0'
            self.A.cast_int8(np.int8(memory_rom.get_celds()[dirc]))
        elif ir_hex[3] == 'F':      #RRCA
            self.F.get_register()[0] = self.A.get_register()[7]
            a = [self.F.get_register()[0]]
            a.extend(a[:7])
            self.A.copy_from_array(a)

    def on_f(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0X1
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == '4':        # INC D
            new_reg = self.alu.increment(self.alu, self.D.cast_int8(), self.F.get_register())
            self.D.copy_from_int8(new_reg)
        elif ir_hex[3] == '5':      # DEC D
            new_reg = self.alu.decrement(self.alu, self.D.cast_int8(), self.F.get_register())
            self.D.copy_from_int8(new_reg)
        elif ir_hex[3] == '7':      #RLA
            #register = [self.F.get_register()[0]]
            register = []
            f_ = self.F.get_register()[0]
            self.F.get_register()[0] = self.A.get_register()[0]
            register.extend(self.A.get_register()[1:])
            register.append(f_)
            self.A.copy_from_array(register)
        elif ir_hex[3] == '8':      # JR e
            e = int ('0X' + ir_hex[5:], 16)
            new_pc = self.alu.add(self.alu, self.PC.cast_int8(), e, self.F.get_register())
            self.PC.copy_from_int8(new_pc)
        elif ir_hex[3] == 'C':      # INC E
            new_reg = self.alu.increment(self.alu, self.E.cast_int8(), self.F.get_register())
            self.E.copy_from_int8(new_reg)
        elif ir_hex[3] == 'D':      # DEC E
            new_reg = self.alu.decrement(self.alu, self.E.cast_int8(), self.F.get_register())
            self.E.copy_from_int8(new_reg)
        elif ir_hex[3] == '6':      # LD D, n
            bits = list (bin(int (self.IR.cast_hex()[4:], 16))[2:])
            self.D.copy_from_array(bits)
        elif ir_hex[3] == 'E':      # LD E, n
            bits = list (bin(int (self.IR.cast_hex()[4:], 16))[2:])
            self.E.copy_from_array(bits)

    def tw_f(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0X2
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == '4':            # INC H
            new_reg = self.alu.increment(self.alu, self.H.cast_int8(), self.F.get_register())
            self.H.copy_from_int8(new_reg)
        if ir_hex[3] == '5':            # DEC H
            new_reg = self.alu.decrement(self.alu, self.H.cast_int8(), self.F.get_register())
            self.H.copy_from_int8(new_reg)
        elif ir_hex[3] == 'C':          # INC L
            new_reg = self.alu.increment(self.alu, self.L.cast_int8(), self.F.get_register())
            self.L.copy_from_int8(new_reg)
        elif ir_hex[3] == 'D':          # DEC L
            new_reg = self.alu.decrement(self.alu, self.L.cast_int8(), self.F.get_register())
            self.L.copy_from_int8(new_reg)
        elif ir_hex[3] == 'F':          # CPL
            new_reg = self.alu.cop_one(self.alu, self.A.get_register(), self.F.get_register())
            self.A.copy_from_array(new_reg)
        elif ir_hex[3] == '6':          # LD H, n
            bits = list (bin(int (self.IR.cast_hex()[4:], 16))[2:])
            self.H.copy_from_array(bits)
        elif ir_hex[3] == 'E':          # LD L, n
            bits = list (bin(int (self.IR.cast_hex()[4:], 16))[2:])
            self.L.copy_from_array(bits)
        elif ir_hex[3] == '8' and self.F.get_register()[6] == '1':      # JR z, e
            e = int ('0X' + ir_hex[5:], 16)
            new_pc = self.alu.add(self.alu, self.PC.cast_int8(), e, self.F.get_register())
            self.PC.copy_from_int8(new_pc)
        elif ir_hex[3] == '0' and self.F.get_register()[6] == '0':      # JR Nz, e
            e = int ('0X' + ir_hex[5:], 16)
            new_pc = self.alu.add(self.alu, self.PC.cast_int8(), e, self.F.get_register())
            self.PC.copy_from_int8(new_pc)


    def th_f(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0X3
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == '4':        # INC HL
            pass
        elif ir_hex[3] == '5':      # DEC HL
            #new_reg = self.alu.decrement(self.alu, self.__get_value_hl__.cast_int8(), self.F.get_register())
            #self.__set_value_hl__.copy_from_int8(new_reg)
            pass
        elif ir_hex[3] == 'A':      #LD A,(nn)
            bits = hex (memory_ram.get_celds()[self.PC.cast_hex()])
            bits = np.int8(int ('0X' + bits[:3:-1] + bits[2:4]))
            self.A.copy_from_int8(bits)
        elif ir_hex[3] == 'C':      # INC A
            new_reg = self.alu.increment(self.alu, self.A.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == 'D':      # DEC A
            new_reg = self.alu.decrement(self.alu, self.A.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == 'F':      # CCF
            self.F.get_register()[1] = self.F.get_register()[4] = 0
            self.F.get_register()[0] = '1' if self.F.get_register()[0] == '0' else '0'
        elif ir_hex[3] == '6':      # LD (HL), n
            hex_ = np.int8(int (ir_hex[4:], 16))
            self.____set_value_hl__(hex_, memory_rom)
        elif ir_hex[3] == 'E':      # LD A, n
            bits = list (bin(int (self.IR.cast_hex()[4:], 16))[2:])
            self.A.copy_from_array(bits)

    def fr_f(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0X4
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == '6':        # LD B, (HL)
            self.B.cast_int8(self.__get_value_hl__(memory_rom))
        elif ir_hex[3] == 'E':      # LD C, (HL)
            self.C.cast_int8(self.__get_value_hl__(memory_rom))

    def fv_f(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0X5
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == '6':        # LD D, (HL)
            self.D.cast_int8(self.__get_value_hl__(memory_rom))
        elif ir_hex[3] == 'E':      # LD E, (HL)
            self.E.cast_int8(self.__get_value_hl__(memory_rom))

    def sx_f(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0X6
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == '6':        # LD H, (HL)
            self.H.cast_int8(self.__get_value_hl__(memory_rom))
        elif ir_hex[3] == 'E':      # LD L, (HL)
            self.L.cast_int8(self.__get_value_hl__(memory_rom))

    def sv_f(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0X7
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == '6':        # LD A, (HL)
            self.A.cast_int8(self.__get_value_hl__(memory_rom))
        elif ir_hex[3] == '0':      #LD (HL) B
            Bval = self.B.cast_hex()
            self.__set_value_hl__(Bval,memory_rom)
        elif ir_hex[3] == '1':      #LD (HL) C
            Cval = self.C.cast_hex()
            self.__set_value_hl__(Cval,memory_rom)
        elif ir_hex[3] == '2':      #LD (HL) D
            Dval = self.D.cast_hex()
            self.__set_value_hl__(Dval,memory_rom)
        elif ir_hex[3] == '3':      #LD (HL) E
            Eval = self.E.cast_hex()
            self.__set_value_hl__(Eval,memory_rom)
        elif ir_hex[3] == '4':      #LD (HL) H
            Hval = self.H.cast_hex()
            self.__set_value_hl__(Hval,memory_rom)
        elif ir_hex[3] == '5':      #LD (HL) L
            Lval = self.L.cast_hex()
            self.__set_value_hl__(Lval,memory_rom)
        elif ir_hex[3] == '7':      #LD (HL) A
            Aval = self.A.cast_hex()
            self.__set_value_hl__(Aval,memory_rom)

    def eg_f(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0X8
        '''

    def ni_f(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0X9
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == '0':        #SUB B
            new_reg = self.alu.sub(self.alu, self.A.cast_int8(), self.B.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == '1':      #SUB C
            new_reg = self.alu.sub(self.alu, self.A.cast_int8(), self.C.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == '2':      #SUB D
            new_reg = self.alu.sub(self.alu, self.A.cast_int8(), self.D.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == '3':      #SUB E
            new_reg = self.alu.sub(self.alu, self.A.cast_int8(), self.E.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == '4':      #SUB H
            new_reg = self.alu.sub(self.alu, self.A.cast_int8(), self.H.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == '5':      #SUB L
            new_reg = self.alu.sub(self.alu, self.A.cast_int8(), self.L.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == '6':      #SUB HL
            new_reg = self.alu.sub(self.alu, self.A.cast_int8() , self.__get_value_hl__(memory_rom), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == '7':      #SUB A
            new_reg = self.alu.sub(self.alu, self.A.cast_int8(), self.A.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)

    def a_fu(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comenza por 0XA
        '''
        ir_hex = self.IR.get_register()
        if ir_hex[4] == '0':
            r_opt = {
                '0': self.B.cast_int8(),
                '1': self.C.cast_int8(),
                '2': self.D.cast_int8(),
                '3': self.E.cast_int8(),
                '4': self.H.cast_int8(),
                '5': self.L.cast_int8(),  
                '7': self.A.cast_int8(),
            }
            a_int8 = self.A.cast_int8()
            r_int8 = r_opt.get(self.IR.cast_hex()[3], self.__get_value_hl__(memory_rom))
            new_register = self.alu.and_logic(self.alu, a_int8, r_int8, self.F.get_register())
            self.A.copy_from_int8(new_register)
        elif ir_hex[3] == '8':        #XOR B
            new_reg = self.alu.xor_logic(self.alu, self.A.cast_int8(), self.B.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == '9':      #XOR C
            new_reg = self.alu.xor_logic(self.alu, self.A.cast_int8(), self.C.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == 'A':      #XOR D
            new_reg = self.alu.xor_logic(self.alu, self.A.cast_int8(), self.D.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == 'B':      #XOR E
            new_reg = self.alu.xor_logic(self.alu, self.A.cast_int8(), self.E.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == 'C':      #XOR H
            new_reg = self.alu.xor_logic(self.alu, self.A.cast_int8(), self.H.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == 'D':      #XOR L
            new_reg = self.alu.xor_logic(self.alu, self.A.cast_int8(), self.L.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == 'E':      #XOR HL
            new_reg = self.alu.xor_logic(self.alu, self.A.cast_int8() , self.__get_value_hl__(memory_rom), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == 'F':      #XOR A
            new_reg = self.alu.xor_logic(self.alu, self.A.cast_int8(), self.A.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        else:
            pass

    def b_fu(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0XB
        '''
        ir_hex = self.IR.get_register()
        if ir_hex[4] == '0':    # AND s
            s_opt = {
                '0': self.B.cast_int8(),
                '1': self.C.cast_int8(),
                '2': self.D.cast_int8(),
                '3': self.E.cast_int8(),
                '4': self.H.cast_int8(),
                '5': self.L.cast_int8(),  
                '7': self.A.cast_int8(),
            }
            a_int8 = self.A.cast_int8()
            s_int8 = s_opt.get(self.IR.cast_hex()[3], self.__get_value_hl__(memory_rom))
            new_register = self.alu.or_logic(self.alu, a_int8, s_int8)
            self.A.copy_from_int8(new_register)
        
            # Acá deben venir las instruciones CP
        elif ir_hex[3] == '8':      #CP B
            self.alu.sub(self.alu, self.A.cast_int8(), self.B.cast_int8(), self.F.get_register())
        elif ir_hex[3] == '9':      #CP C
            cp = self.alu.sub(self.alu, self.A.cast_int8(), self.C.cast_int8(), self.F.get_register())
        elif ir_hex[3] == 'A':      #CP D
            cp = self.alu.sub(self.alu, self.A.cast_int8(), self.D.cast_int8(), self.F.get_register())
        elif ir_hex[3] == 'B':      #CP E
            cp = self.alu.sub(self.alu, self.A.cast_int8(), self.E.cast_int8(), self.F.get_register())
        elif ir_hex[3] == 'C':      #CP H
            cp = self.alu.sub(self.alu, self.A.cast_int8(), self.H.cast_int8(), self.F.get_register())
        elif ir_hex[3] == 'D':      #CP L
            cp = self.alu.sub(self.alu, self.A.cast_int8(), self.L.cast_int8(), self.F.get_register())
        elif ir_hex[3] == 'E':      #CP HL
            cp = self.alu.sub(self.alu, self.A.cast_int8() , self.__get_value_hl__(memory_rom), self.F.get_register())
        elif ir_hex[3] == 'F':      #CP A
            cp = self.alu.sub(self.alu, self.A.cast_int8(), self.A.cast_int8(), self.F.get_register())
        else:    
            pass

    def c_fu(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0XC
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == '3':        # JP nn
            new_register = self.alu.increment(self.alu, self.PC.get_register(), self.F.get_register())
            self.PC.copy_from_int8(new_register)
            bits = hex (memory_ram.get_celds()[self.PC.cast_hex()])
            bits = np.int8(int ('0X' + bits[:3:-1] + bits[2:4]))
            self.PC.copy_from_int8(bits)
        if ir_hex[3] == 'B':        # Operation bits
            if ir_hex[4] == '0':        # Operation RLC r ,RRC m
                register = []
                if ir_hex[5] == '0':    # RLC B
                    self.F.get_register()[0] = self.B.get_register()[0]
                    register.extend(self.B.get_register[1:])
                    register.append(self.F.get_register()[0])
                    self.B.copy_from_array(register)
                elif ir_hex[5] == '1':  # RLC C
                    self.F.get_register()[0] = self.D.get_register()[0]
                    register.extend(self.C.get_register[1:])
                    register.append(self.F.get_register()[0])
                    self.C.copy_from_array(register)
                elif ir_hex[5] == '2':  # RLC D
                    self.F.get_register()[0] = self.D.get_register()[7]
                    register.extend(self.D.get_register[1:])
                    register.append(self.F.get_register()[0])
                    self.D.copy_from_array(register)
                elif ir_hex[5] == '3':  # RLC E
                    self.F.get_register()[0] = self.E.get_register()[0]
                    register.extend(self.E.get_register[1:])
                    register.append(self.F.get_register()[0])
                    self.E.copy_from_array(register)
                elif ir_hex[5] == '4':  # RLC H
                    self.F.get_register()[0] = self.H.get_register()[0]
                    register.extend(self.H.get_register[1:])
                    register.append(self.F.get_register()[0])
                    self.H.copy_from_array(register)
                elif ir_hex[5] == '5':  # RLC L
                    self.F.get_register()[0] = self.L.get_register()[0]
                    register.extend(self.L.get_register[1:])
                    register.append(self.F.get_register()[0])
                    self.L.copy_from_array(register)
                elif ir_hex[5] == '6':  # RLC HL
                    hl = np.binary_repr(self.__get_value_hl__(memory_rom)[2:], 8)
                    self.F.get_register()[0] = hl[0]
                    register.extend(hl[1:])
                    register.append(self.F.get_register()[0])
                    hex_ = np.int8(int(''.join(register), 2))
                    self.__set_value_hl__(hex_, memory_rom)
                elif ir_hex[5] == '7':   # RLC A
                    self.F.get_register()[0] = self.A.get_register()[0]
                    register.extend(self.A.get_register[1:])
                    register.append(self.F.get_register()[0])
                    self.A.copy_from_array(register)
                elif ir_hex[5] == '8':    # RRC B
                    self.F.get_register()[0] = self.B.get_register()[7]
                    register.append(self.F.get_register()[0])
                    register.extend(self.B.get_register[0:7])
                    self.B.copy_from_array(register)
                elif ir_hex[5] == '9':  # RRC C
                    self.F.get_register()[0] = self.C.get_register()[7]
                    register.append(self.F.get_register()[0])
                    register.extend(self.C.get_register[0:7])
                    self.C.copy_from_array(register)
                elif ir_hex[5] == 'A':  # RRC D
                    self.F.get_register()[0] = self.D.get_register()[7]
                    register.append(self.F.get_register()[0])
                    register.extend(self.D.get_register[0:7])
                    self.D.copy_from_array(register)
                elif ir_hex[5] == 'B':  # RRC E
                    self.F.get_register()[0] = self.E.get_register()[7]
                    register.append(self.F.get_register()[0])
                    register.extend(self.E.get_register[0:7])
                    self.E.copy_from_array(register)
                elif ir_hex[5] == 'C':  # RRC H
                    self.F.get_register()[0] = self.H.get_register()[7]
                    register.append(self.F.get_register()[0])
                    register.extend(self.H.get_register[0:7])
                    self.H.copy_from_array(register)
                elif ir_hex[5] == 'D':  # RRC L
                    self.F.get_register()[0] = self.L.get_register()[7]
                    register.append(self.F.get_register()[0])
                    register.extend(self.L.get_register[0:7])
                    self.L.copy_from_array(register)
                elif ir_hex[5] == 'E':  # RRC HL
                    hl = np.binary_repr(self.__get_value_hl__(memory_rom)[2:], 8)
                    self.F.get_register()[0] = hl[7]
                    register.append(self.F.get_register()[0])
                    register.extend(hl[0:7])
                    hex_ = np.int8(int(''.join(register), 2))
                    self.__set_value_hl__(hex_, memory_rom)
                elif ir_hex[5] == 'F':   # RRC A
                    self.F.get_register()[0] = self.A.get_register()[7]
                    register.append(self.F.get_register()[0])
                    register.extend(self.A.get_register[0:7])
                    self.A.copy_from_array(register)
            elif ir_hex[4] == '1':      # Operation RL r
                register = [self.F.get_register()[0]]
                f_ = self.F.get_register()[0]
                if ir_hex[5] == '0':    # RL B
                    self.F.get_register()[0] = self.B.get_register()[0]
                    register.extend(self.B.get_register()[1:])
                    register.append(f_)
                    self.B.copy_from_array(register)
                elif ir_hex[5] == '1':  # RL C
                    self.F.get_register()[0] = self.C.get_register()[0]
                    register.extend(self.C.get_register()[1:])
                    register.append(f_)
                    self.C.copy_from_array(register)
                elif ir_hex[5] == '2':  # RL D
                    self.F.get_register()[0] = self.D.get_register()[0]
                    register.extend(self.D.get_register()[1:])
                    register.append(f_)
                    self.D.copy_from_array(register)
                elif ir_hex[5] == '3':  # RL E
                    self.F.get_register()[0] = self.E.get_register()[0]
                    register.extend(self.E.get_register()[1:])
                    register.append(f_)
                    self.E.copy_from_array(register)
                elif ir_hex[5] == '4':  # RL H
                    self.F.get_register()[0] = self.H.get_register()[0]
                    register.extend(self.H.get_register()[1:])
                    register.append(f_)
                    self.H.copy_from_array(register)
                elif ir_hex[5] == '5':  # RL L
                    self.F.get_register()[0] = self.L.get_register()[0]
                    register.extend(self.L.get_register()[1:])
                    register.append(f_)
                    self.L.copy_from_array(register)
                elif ir_hex[5] == '6':  # RL (HL)
                    hl = list (np.binary_repr(self.__get_value_hl__(memory_rom), 8))
                    self.F.get_register()[0] = hl[0]
                    register.extend(hl[1:])
                    register.append(f_)
                    hex_ = np.int8(int (''.join(register), 2))
                    self.__set_value_hl__(hex_, memory_rom)
                elif ir_hex[5] == '7':  # RL A
                    self.F.get_register()[0] = self.A.get_register()[0]
                    register.extend(self.A.get_register()[1:])
                    register.append(f_)
                    self.A.copy_from_array(register)
                elif ir_hex[5] == '8':    # RR B
                    #register = [self.F.get_register()[0]]
                    #f_ = self.F.get_register()[0]
                    self.F.get_register()[0] = self.B.get_register()[7]
                    register.extend(self.B.get_register()[0:7])
                    self.B.copy_from_array(register)
                elif ir_hex[5] == '9':  # RR C
                    self.F.get_register()[0] = self.C.get_register()[7]
                    register.extend(self.C.get_register()[0:7])
                    self.C.copy_from_array(register)
                elif ir_hex[5] == 'A':  # RR D
                    self.F.get_register()[0] = self.D.get_register()[7]
                    register.extend(self.D.get_register()[0:7])
                    self.D.copy_from_array(register)
                elif ir_hex[5] == 'B':  # RR E
                    self.F.get_register()[0] = self.E.get_register()[7]
                    register.extend(self.E.get_register()[0:7])
                    self.E.copy_from_array(register)
                elif ir_hex[5] == 'C':  # RR H
                    self.F.get_register()[0] = self.H.get_register()[7]
                    register.extend(self.H.get_register()[0:7])
                    self.H.copy_from_array(register)
                elif ir_hex[5] == 'D':  # RR L
                    self.F.get_register()[0] = self.L.get_register()[7]
                    register.extend(self.L.get_register()[0:7])
                    self.L.copy_from_array(register)
                elif ir_hex[5] == 'E':  # RR (HL)
                    hl = list (np.binary_repr(self.__get_value_hl__(memory_rom), 8))
                    self.F.get_register()[0] = hl[7]
                    register.extend(hl[0:7])
                    hex_ = np.int8(int (''.join(register), 2))
                    self.__set_value_hl__(hex_, memory_rom)
                elif ir_hex[5] == 'F':  # RR A
                    self.F.get_register()[0] = self.A.get_register()[7]
                    register.extend(self.A.get_register()[0:7])
                    self.A.copy_from_array(register)
            elif ir_hex[4] == '2':      # Operation SLA m
                register = []
                if ir_hex[5] == '0':    # SLA B
                    self.F.get_register()[0] = self.B.get_register()[0]
                    register.extend(self.B.get_register()[1:])
                    register.append('0')
                    self.B.copy_from_array(register)
                elif ir_hex[5] == '1':  # SLA C
                    self.F.get_register()[0] = self.C.get_register()[0]
                    register.extend(self.C.get_register()[1:])
                    register.append('0')
                    self.C.copy_from_array(register)
                elif ir_hex[5] == '2':  # SLA D
                    self.F.get_register()[0] = self.D.get_register()[0]
                    register.extend(self.D.get_register()[1:])
                    register.append('0')
                    self.D.copy_from_array(register)
                elif ir_hex[5] == '3':  # SLA E
                    self.F.get_register()[0] = self.E.get_register()[0]
                    register.extend(self.E.get_register()[1:])
                    register.append('0')
                    self.E.copy_from_array(register)
                elif ir_hex[5] == '4':  # SLA H
                    self.F.get_register()[0] = self.H.get_register()[0]
                    register.extend(self.B.get_register()[1:])
                    register.append('0')
                    self.H.copy_from_array(register)
                elif ir_hex[5] == '5':  # SLA L
                    self.F.get_register()[0] = self.L.get_register()[0]
                    register.extend(self.L.get_register()[1:])
                    register.append('0')
                    self.L.copy_from_array(register)
                elif ir_hex[5] == '6':  # SLA (HL)
                    hl = list (np.binary_repr(self.__get_value_hl__(memory_rom), 8))
                    self.F.get_register()[0] = hl[0]
                    register.extend(hl[1:])
                    register.append('0')
                    hex_ = np.int8(int (''.join(register), 2))
                    self.__set_value_hl__(hex_, memory_rom)
                elif ir_hex[5] == '7':  # SLA A
                    self.F.get_register()[0] = self.A.get_register()[0]
                    register.extend(self.A.get_register()[1:])
                    register.append('0')
                    self.A.copy_from_array(register)
            elif ir_hex[4] == '3':      # Operation SLA m
                register = ['0']
                if ir_hex[5] == '8':    # SRL B
                    self.F.get_register()[0] = self.B.get_register()[7]
                    register.extend(self.B.get_register()[:7])
                    self.B.copy_from_array(register)
                elif ir_hex[5] == '9':  # SRL C
                    self.F.get_register()[0] = self.C.get_register()[7]
                    register.extend(self.C.get_register()[:7])
                    self.C.copy_from_array(register)
                elif ir_hex[5] == 'A':  # SRL D
                    self.F.get_register()[0] = self.D.get_register()[7]
                    register.extend(self.D.get_register()[:7])
                    self.D.copy_from_array(register)
                elif ir_hex[5] == 'B':  # SRL E
                    self.F.get_register()[0] = self.E.get_register()[7]
                    register.extend(self.E.get_register()[:7])
                    self.E.copy_from_array(register)
                elif ir_hex[5] == 'C':  # SRL H
                    self.F.get_register()[0] = self.H.get_register()[7]
                    register.extend(self.H.get_register()[:7])
                    self.H.copy_from_array(register)
                elif ir_hex[5] == 'D':  # SRL L
                    self.F.get_register()[0] = self.L.get_register()[7]
                    register.extend(self.L.get_register()[:7])
                    self.L.copy_from_array(register)
                elif ir_hex[5] == 'E':    # SRL (HL)
                    hl = list (np.binary_repr(self.__get_value_hl__(memory_rom), 8))
                    self.F.get_register()[0] = hl[7]
                    register.extend(hl[:7])
                    hex_ = np.int8(int (''.join(register), 2))
                    self.__set_value_hl__(hex_, memory_rom)
                elif ir_hex[5] == 'F':  # SRL A
                    self.F.get_register()[0] = self.A.get_register()[7]
                    register.extend(self.A.get_register()[:7])
                    self.A.copy_from_array(register)
        elif ir_hex[3] == '6':      #ADD A,n
            n = list (bin(int (self.IR.cast_hex()[4:], 16))[2:])
            new_reg = self.alu.add(self.alu, self.A.cast_int8(), self.n.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == '9':      #RET
            #acceder al valor de la memoria con direccion SP
            pc_hex1 = self.PC.cast_hex()
            memVal1 = memory_ram.get_celds()[self.SP.cast_hex()]
            #Cambiar el valor del PC[8:] al valor anterior
            self.PC[8:] = memVal1
            #incrementar en 1 el valor del SP
            new_sp = self.alu.increment(self.alu, self.SP.cast_int8(), ['0' for _ in range(8)])
            self.SP.copy_from_int8(new_sp)
            #acceder al valor de la memoria con direccion SP
            pc_hex2 = self.PC.cast_hex()
            memVal2 = memory_ram.get_celds()[self.SP.cast_hex()]
            #Cambiar el valor del PC[0:8] al valor anterior
            self.PC[0:8] = memVal2
            #incrementar en 1 el valor del SP
            new_sp = self.alu.increment(self.alu, self.SP.cast_int8(), ['0' for _ in range(8)])
            self.SP.copy_from_int8(new_sp)





    def d_fu(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0XD
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == 'B':
            n = np.int8(int (in_byte, 16))
            self.A.copy_from_int8(n)
        if ir_hex[3] == '6':#SUB n
            n = np.int8(int (in_byte, 16))
            new_reg = self.alu.sub(self.alu, self.A.cast_int8(), n, self.F.get_register())
            self.A.copy_from_int8(new_reg)


    def e_fu(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0XE
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == 'E':#XOR n
            n = list (bin(int (self.IR.cast_hex()[4:], 16))[2:])
            new_reg = self.alu.xor_logic(self.alu, self.A.cast_int8(), self.n.cast_int8(), self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == 'D' and ir_hex[4] == '4' and ir_hex[5] == '4':    #NEG
            zero = np.int8(0);
            new_reg = self.alu.sub(self.alu, self.A.cast_int8(), zero, self.F.get_register())
            self.A.copy_from_int8(new_reg)
        elif ir_hex[3] == 'D' and ir_hex[4] == 'A' and ir_hex[5] == '2':    #INI
            i = np.int16(int(input()))
            self.H.copy_from_array(i[0:8])
            self.L.copy_from_array(i[8:])
        elif ir_hex[3] == 'D' and ir_hex[4] == 'A' and ir_hex[5] == '3':    #OUTI
            i1 = [self.H]
            i2 = i1.extend([self.L])
            print(np.int16(i2))


    def f_fu(self, memory_rom, memory_ram, in_byte):
        '''
            Se revisa cual de todas las funciones cullo OpCode comienza por 0XF
        '''
        ir_hex = self.IR.cast_hex()
        if ir_hex[3] == 'E':#CP n
            n = list (bin(int (self.IR.cast_hex()[4:], 16))[2:])
            cp = self.alu.sub(self.alu, self.A.cast_int8(), self.n.cast_int8(), self.F.get_register())

    __ISA = {
        '0X0': ze_f,
        '0X1': on_f,
        '0X2': tw_f,
        '0X3': th_f,
        '0X4': fr_f,
        '0X5': fv_f,
        '0X6': sx_f,
        '0X7': sv_f,
        '0X8': eg_f,
        '0X9': ni_f,
        '0XA': a_fu,
        '0XB': b_fu,
        '0XC': c_fu,
        '0XD': d_fu,
        '0XE': e_fu,
        '0XF': f_fu
    }
