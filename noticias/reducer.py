import sys

most_relevant = (0, "")  # Inicializar relevancia y noticia vacía

for line in sys.stdin:
    try:
        relevancia, noticia = line.strip().split("\t", 1)
        relevancia = int(relevancia)
        
        # Comparar y actualizar la noticia más relevante
        if relevancia > most_relevant[0]:
            most_relevant = (relevancia, noticia)
    except Exception as e:
        continue

print(f"{most_relevant[0]}\t{most_relevant[1]}")
