#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

# Leer cada línea de la entrada estándar
for line in sys.stdin:
    # Eliminar espacios en blanco al inicio y al final
    line = line.strip()
    # Dividir la línea en palabra y conteo
    word, count = line.split('\t', 1)
    
    try:
        count = int(count)
    except ValueError:
        continue  # Si el conteo no es un número, ignorar la línea

    # Si la palabra es la misma que la anterior, sumar el conteo
    if current_word == word:
        current_count += count
    else:
        # Si no es la misma palabra, imprimir el conteo de la anterior
        if current_word:
            print(f"{current_word}\t{current_count}")
        # Cambiar a la nueva palabra
        current_word = word
        current_count = count

# Imprimir el conteo de la última palabra
if current_word == word:
    print(f"{current_word}\t{current_count}")