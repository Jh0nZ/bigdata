import sys
import re

for line in sys.stdin:
    palabras = line.strip().lower().split()
    for palabra in palabras:
        if palabra.isalpha():  # Filtra palabras que solo contienen letras
            print(f"{palabra}\t1")
