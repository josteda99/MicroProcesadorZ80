import Componente as com
import numpy as np

alu = com.ALU()
num1 = np.int8(-71)
num2 = np.int8(-114)
flags = [0 for _ in range(8)]

print(alu.and_logic(num1, num2, flags))

# var1 = int (input("entero1\n"), base=2)

# var2 = int (input("entero2\n"), base=2)

# var3 = var1 + var2

# s_var = bin (var3)
# c = s_var.split('b')

# print(c, type(c))
# print(bin(var3), var3)
