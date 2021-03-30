import Componente as com
import numpy as np

# Crear una clase processor
# Crear una RAM y ROM

m = com.Memory()
m.celds['0x0'] = 0xA7

p = com.Processor()

p.fetch(m)