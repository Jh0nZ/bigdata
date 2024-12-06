import sys

# Inicializar la variable para la tarifa mínima
precio_minimo = float('inf')  # Valor inicial muy alto

# Inicializar la clave para comparar las combinaciones de ciudad, tipo de conexión y plan
clave_actual = None

for line in sys.stdin:
    try:
        # Leer la clave y el valor
        clave, precio = line.strip().split("\t")
        clave = eval(clave)  # Convertir la clave a una tupla
        precio = int(precio)  # Convertir el precio a entero

        # Comparar si el precio es el mínimo para esa clave
        if precio < precio_minimo:
            clave_actual = clave
            precio_minimo = precio

    except Exception as e:
        continue

# Imprimir la última clave y el precio mínimo
if clave_actual is not None:
    print(f"{clave_actual}\t{precio_minimo}")
else:
    print("No se encontraron datos válidos")
