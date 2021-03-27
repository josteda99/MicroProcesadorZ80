import Componente as com
import numpy as np

# Crear una clase processor
# Crear una RAM y ROM

h = 0xAA
print(type(h))

alu = com.ALU()
num1 = np.int8(-72)
num2 = np.int8(-14)

rg = com.Register(8)

m = com.Memory()

print(alu.and_logic(num1, num2, rg.get_register()))

print(rg.get_register())