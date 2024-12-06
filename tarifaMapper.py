#!/usr/bin/env python3
import sys

# Leer cada línea de la entrada estándar
for line in sys.stdin:
    # Eliminar espacios en blanco al inicio y al final
    line = line.strip()
    # Dividir la línea en palabras
    words = line.split()
    # Emitir cada palabra con un conteo de 1
    for word in words:
        print(f"{word}\t1")