import Componente as com
import numpy as np

# Crear una clase processor
# Crear una RAM y ROM

m_ram = com.Memory()
p = com.Processor()
on = True

while on:
    if len(m_ram.get_celds()) == 0:
        on = com.loader(m_ram, p)
        if not on:
            break 
        m_ram.print_info()
    p.fetch(m_ram)
    p.decode(m_ram)