import Componente as com
import numpy as np

# Crear una clase processor
# Crear una RAM y ROM

m_ram = com.Memory()
m_ram.get_celds()['0X0000'] = np.int8(0X06F1)
m_rom = com.Memory()
m_rom.get_celds()['0X0000'] = np.int8(0XA100)

f = ['0' for _ in range(8)]
a = ['1', '0', '1', '1', '1', '0', '1', '0']
a_1 = '0XFEFF'
a_ = ['0']

bits = np.int16(int (a_1, 16))
br = np.binary_repr(bits, 16)
b = br[8:] + br[0:8]
print(hex(int (b, 2)))
print(b)
# print(list(np.binary_repr(np.int8(int ("A2", 16)), 8)))     # De un np.int8 a una lista de bits
# print(np.int8(int(''.join(a), 2)))          # castear de una lista de bits a un np.int8
p = com.Processor()

f[0] = a[7]
a_.extend(a[:7])
# print(a)
# print(a_)
# print(f)