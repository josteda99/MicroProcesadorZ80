# MicroProcesadorZ80
Emulacion en python del Microprocesador Z80 considerando e implementando ciertas caracteristicas de su arquitectura interna tales como son los registros, el acumulador,
la Unidad Logica aritmetica (ALU) que este contiene, sin embargo, solo emulara 50 de sus instrucciones de maquina (ISA).

# Convenciones 
Para mas estrictos con respecto a la emulacion se harán las indexaciones de memoria (RAM, ROM) en base hexadecimal y se las operaciones aritmetico-logicas en base binaria.

...Agregar la seccionde las Instruciones y una explicacion de como se debe usar...

## ALU
Funciones a emular 
- Sumar
- Restar
- And
- Or
- Xor
- Compera ??
- Desplazar bit (Izquierda, Derecha)
- Incrementar Decrementar
- Set bit

## Registros
**Registros acumuladores y flag**, cada flag esta implementado comoun registro con la siguiente distribbución: _**flag[6]**: ZERO_, _**flag[7]**: Sign_, _**flag[0]**: Carry_, _**flag[2]**: OverFlow_, _**flag[1] y flag[4]**: N (ultima operacion una suma '0' o resta '1')_; estos registros son de 8-bit sacumulador y Flag respectivamente .
- A, F (Principales)
- A', F'

Solo se implementaran los registros principales, posee **registors de propocito general** los cuales son implementados para realizar operaciones con el registro acumulador y _flag_ que se encuentre activo, estos resgistros son de 8-bits. 
- A, B, C, D, E, H, L
**Registos de Propocito especifico** 
- PC (Program Counter) 16-bits
- SP (Stack Pointer) 16-bits
- IR (Instructon Register) 16-bits


## Bibliografia
http://redeya.bytemaniacos.com/electronica/tutoriales/Z80/z80.html
http://galia.fc.uaslp.mx/~cantocar/microprocesadores/TUTORIALES/EL_MICRO_Z80/ARQUITECTURA_DEL_MICROPROCE.HTM
https://wiki.python.org/moin/BitManipulation
https://clrhome.org/table/