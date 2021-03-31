import Componente as com
import numpy as np

# Crear una clase processor
# Crear una RAM y ROM

def print_uno():
    print("Es un uno")

def switch(args):
    dic = {
        'A' : 1,
        '1' : print_uno(),
    }
    return dic.get(args, 'No esta')

m_ram = com.Memory()
m_ram.get_celds()['0X0'] = 0X06F1
m_rom = com.Memory()
m_rom.get_celds()['0X0'] = 0XA1

c = np.int8(0XA2)
b = np.int8(int("10101110", 2))
d = np.int8(15)

h, l= '0XF9', '0XB1'
hl = '0X' + h[2:] + l[2:]

h = h[2:]
v = bin(int (h, 16))
# print(v)
# print(hl)
# print(c, b, d, sep=" ")
# print('0' <= '7')

p = com.Processor()
p.fetch(m_ram)
p.decode(m_rom)