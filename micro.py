# ALU
    # sumar
    # restar
    # AND
    # OR
    # XOR
    # comparar
    # desplazar bit der
    # desplazar bit izq
    # rotar
    # incremento
    # decremento
    # set_bit
# Escribir
# leer
# memoria como Array? Hash?
# jumpers
# ACU
# Mux
# paro
# espera
# requision de interrupcion mascarable
# interrupcion no mascaro
# reset
# reloj

var1 = int (input("entero1\n"), base=2)

var2 = int (input("entero2\n"), base=2)

var3 = var1 + var2

s_var = bin (var3)
c = s_var.split('b')

print(c, type(c))
# print(bin(var3), var3)