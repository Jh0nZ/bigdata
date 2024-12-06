import sys
import re

longitud_minima = 0

for line in sys.stdin:
    palabras = line.strip().lower().split()
    for palabra in palabras:
        if palabra.isalpha() and len(palabra) >= longitud_minima:
        #if palabra.isalpha():  # Filtra palabras que solo contienen letras
            print(f"{palabra}\t1")
