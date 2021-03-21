import Componente as com

alu = com.ALU()

flags = [0 for _ in range(8)]

print(alu.add(0b11001010, 0b11100011, flags))

print(flags)

# var1 = int (input("entero1\n"), base=2)

# var2 = int (input("entero2\n"), base=2)

# var3 = var1 + var2

# s_var = bin (var3)
# c = s_var.split('b')

# print(c, type(c))
# print(bin(var3), var3)