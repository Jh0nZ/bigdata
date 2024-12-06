import sys
import csv

departamento_filtro = "Cochabamba"
tecnologia_filtro = "FIBRA"
plan_vigente_comercializacion_filtro = "SI"

for line in sys.stdin:
    # Leer cada línea del archivo CSV
    reader = csv.reader([line.strip()])
    for row in reader:
        try:
            # Extraer los valores relevantes de cada fila
            id_tarifa, razon_social, nombre_comercial, departamento, descripcion, costo_instalacion, tipo_pago, otros_beneficios, nombre_tarifa_plan, ancho_banda_bajada, precio_mensual, ancho_banda_subida, denominacion_tecnologia, plan_vigente_comercializacion = row

            # Comprobar si los valores relevantes son válidos
            if departamento == departamento_filtro and denominacion_tecnologia == tecnologia_filtro and precio_mensual.isdigit():
                if plan_vigente_comercializacion_filtro == "TODOS" or plan_vigente_comercializacion == plan_vigente_comercializacion_filtro:
                    # Emisión de clave-valor: clave = (departamento, tecnologia, plan), valor = precio
                    clave = (departamento, denominacion_tecnologia, plan_vigente_comercializacion, nombre_comercial, ancho_banda_bajada, ancho_banda_subida)
                    valor = int(precio_mensual)
                    print(f"{clave}\t{valor}")
        except Exception as e:
            continue
