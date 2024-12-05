import csv

# Abrir el archivo CSV para leer los valores de "Nodes_en"
nodes_en_values = set()

with open("noticias_deber.csv", mode="r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Recorrer las filas del archivo CSV y agregar los valores de "Nodes_en" al set
    for row in csv_reader:
        nodes_en_values.update(row["Nodes_en"].split(", "))

# Imprimir los valores distintos de "Nodes_en"
print("Valores distintos de 'Nodes_en':")
for value in nodes_en_values:
    print(value)


