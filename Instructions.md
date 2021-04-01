# Intrucciones
Los registros de propocito general se encuentran indexados de la siguiente manera:
    A 111, B 000, C 001, D 001, E 011, H 100, L 101

1. 8-bit arithmetic group
    - ADD A, r (suma el registro _r_ en el acumulador).
    - ADD A, n (suma el entetro _n_ al acumulador).
    - SUB s (resta cualquiera de estas operaciones _r, n, (HL)_ en el acumulador).
    - AND s (and entre el acumulador y cualquiera de estas operaciones _r, n, (HL)_).
    - OR s (or entre el acumulador y cualquiera de estas operaciones _r, n, (HL)_).
    - XOR s (xor entre el acumulador y cualquiera de estas operaciones _r, n, (HL)_).
    - CP s (Compara si el acumulador es cero, pero no lo afecta s puede se _r, n, (HL)_).
    - INC r (incrementa el registro r 'Tener en cuenta la bandera **_Oferflow_**').
    - INC (HL) (incrementa el valor de memoria en la direcion _(HL)_).
    - DEC m (decrementa el contenido que se encuentra en m 'Tener en cuenta la bandera **_Oferflow_**').
2. General purpose
    - CPL (complemento A1, negacion del acumulador).
    - NEG (complemento A2, hacer 0 - A en el acumulador 'Tener en cuenta la bandera **_Oferflow_** y **Carry_**'). 
    - CCF (la bandera Carry en el registro F se invierte)
    - SCF (la bandera de Carry en el registro f se cambia)
    - NOP (sleep, no hace nada)
    - HALT (suspende hasta una interrupcion posterior o se recibe un reinicio)
3. 8-bits Load group
    - LD r, r' (copia lo del registro r en r')
    - LD r, n (carga en el registro r un entero n)
    - LD r, (HL) (carga el contenido de la celda de direcion de memoria al registro r)
    - LD (HL), r (almacena en memoria lo del registro r)
    - LD (HL), n (almacena en memoria un entero n)
    - LD A, (BC) (maneja conjunto los registros BC para representar una direccion de memoria y lo carca en el acumulador)(opcional)
    - LD A, (DE) (maneja conjunto los registros DE para representar una direccion de memoria y lo carca en el acumulador)(opcional)
    - LD (BC), A (inversos)(opcional)
    - LD (DE), A (inversos)(opcional)
    - LD (nn), A (inversos)(opcional)
4. Jump group
    - JP nn (mueve el registro PC a la direccion representada por los enteros nn)
    - JP cc, nn (si cc true, PC cargado con nn, revisar pag 259 de Z80CPU)
    - JR e (aumenta PC e veces)
    - JR C, e (aumenta PC e veces si Carry)
    - JR NC, e (aumenta PC e veces si No Carry)
    - JR Z, e (aumenta PC e veces si Zero)
    - JR NZ, e (aumenta PC e veces si No Zero)
    - JP (HL) (aumenta PC el valor que haya en la direccion de memoria de HL)
5. Call and Return group
    - CALL nn (asignar a PC los valores de nn y almacenar por separado sus valores, primero los bytes de mayor grado)
    - CALL cc, nn (asigna al PC los valores de nn si CC True)
    - RET (retorna el PC a su posicion original)
    - RET cc (retorna el PC a su posicion si CC true)
6. Input and Output group
    - IN A, (n) (recibe de un I/O y lo carga en el acumulador)
    - IN r (recibe de un I/O y lo carga en el registro r)
    - INI (recibe I/O y guarda en la direccion _(HL)_ de memoria)
    - OUT A (se imprimir el acumulador)
    - OUT (C), r (se imprime el registro r)
    - OUTI (imprime la direccion de _(HL)_ de memoria)
7. Rotate and swift group
    - RLCA (rotar 1 bit a la izquierda y el bit de signo se copia en Carry)
    - RLA (revisar pag 211)
    - RRCA (el contenido del acumulador se rota 1 bit a la derecha y el bit 0 es copiado en el carry y en el bit 7)
    - RRA (revisar pag 213)
    - RLC r (rotar el registro r a la izquierda y lo que hay en el bit 7 es copiado en el carry y en el bit 0)
    - RLC (HL) (rotar para una posicion de memoria a la izquierda y lo que hay en el bit 7 es copiado en el carry y en el bit 0)
    - RL m (revisar pag 222) 
    - RRC m (revisar pag 225)
    - RR m (revisar pag 228)
    - SLA m (revisar pag 231)
    - SRA m (revisar pag 234)
    - SRL m (revisar pag 237)