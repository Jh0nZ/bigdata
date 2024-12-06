import sys
import csv
from datetime import datetime

# Rango de fechas a filtrar
start_date = datetime.strptime("29/11/2024", '%d/%m/%Y') 
end_date = datetime.strptime("04/12/2024", '%d/%m/%Y') 

for line in sys.stdin:
    # Leer CSV
    reader = csv.reader([line.strip()])
    for row in reader:
        try:
            fecha, titulo, sumario, enlace, fuente = row
            
            # Convertir la fecha a formato datetime
            noticia_date = datetime.strptime(fecha, '%d/%m/%Y')
            
            # Filtrar por rango de fechas
            if start_date <= noticia_date <= end_date:
                # Calcular relevancia
                relevancia = len((sumario + " " + titulo).split())  # Número de palabras en el sumario mas titulo
                
                # Emitir clave-valor
                print(f"{relevancia}\t{fecha},{titulo},{sumario},{enlace},{fuente}")
        except Exception as e:
            continue
