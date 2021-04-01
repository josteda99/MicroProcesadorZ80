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

h, l= '0XF9', '0XB1'
hl = '0X' + h[2:] + l[2:]

v = list (bin(int (hl[4:], 16)))[2:]

p = com.Processor()
p.fetch(m_ram)
p.decode(m_rom)
print(m_rom.get_celds())
p.set_value_hl('2A', m_rom)
print(m_rom.get_celds())