import tkinter as tk
from tkinter import ttk
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Iniciar una sesión de Spark
spark = SparkSession.builder.appName("TarifaMasBaja").getOrCreate()

# Cargar el archivo CSV en un DataFrame
df = spark.read.csv("hdfs:///datos/tarifas.csv", header=True, inferSchema=True)

# Obtener los departamentos y tipos de conexión únicos
departamentos = df.select("DEPARTAMENTO").distinct().rdd.flatMap(lambda x: x).collect()
tipos_conexion = df.select("DENOMINACION_TECNOLOGIA").distinct().rdd.flatMap(lambda x: x).collect()

# Opciones para el nuevo selector
planes_vigentes = ["Todos", "SI", "NO"]

# Función para mostrar la tarifa mínima
def mostrar_tarifa():
    tipo_conexion = tipo_conexion_var.get()
    ciudad = ciudad_var.get()
    plan_vigente = plan_vigente_var.get()
    
    # Filtrar el DataFrame
    df_filtrado = df.filter((df["DENOMINACION_TECNOLOGIA"] == tipo_conexion) & (df["DEPARTAMENTO"] == ciudad))
    
    # Aplicar el filtro de PLAN_VIGENTE_COMERCIALIZACION si no es "Todos"
    if plan_vigente != "Todos":
        df_filtrado = df_filtrado.filter(df["PLAN_VIGENTE_COMERCIALIZACION"] == plan_vigente)

    # Comprobar si hay resultados después del filtrado
    if df_filtrado.count() == 0:
        label_resultado.config(text="No se encontraron tarifas.")
        return

    # Obtener el precio mínimo
    tarifa_minima = df_filtrado.orderBy("PRECIO_MENSUAL").limit(1).first()
    
    print(tarifa_minima)
    
    if tarifa_minima:
        label_resultado.config(text=f"Precio Mínimo en {ciudad} ({tipo_conexion}): {tarifa_minima['PRECIO_MENSUAL']} Bs, Operador: {tarifa_minima['NOMBRE_COMERCIAL']}, Velocidad de Bajada: {tarifa_minima['ANCHO_BANDA_BAJADA']} Mbps.")
    else:
        label_resultado.config(text="No se encontraron tarifas.")

# Crear la ventana principal
root = tk.Tk()
root.title("Consulta de Tarifas")

# Variables para los selectores
ciudad_var = tk.StringVar()
tipo_conexion_var = tk.StringVar()
plan_vigente_var = tk.StringVar()

# Crear los selectores
ttk.Label(root, text="Selecciona un Departamento:").grid(column=0, row=0, padx=10, pady=10)
ciudad_combobox = ttk.Combobox(root, textvariable=ciudad_var, values=departamentos)
ciudad_combobox.grid(column=1, row=0, padx=10, pady=10)

ttk.Label(root, text="Selecciona un Tipo de Conexión:").grid(column=0, row=1, padx=10, pady=10)
tipo_combobox = ttk.Combobox(root, textvariable=tipo_conexion_var, values=tipos_conexion)
tipo_combobox.grid(column=1, row=1, padx=10, pady=10)

ttk.Label(root, text="Selecciona Plan Vigente:").grid(column=0, row=2, padx=10, pady=10)
plan_combobox = ttk.Combobox(root, textvariable=plan_vigente_var, values=planes_vigentes)
plan_combobox.grid(column=1, row=2, padx=10, pady=10)

# Botón para mostrar el resultado
boton_mostrar = ttk.Button(root, text="Mostrar Tarifa Mínima", command=mostrar_tarifa)
boton_mostrar.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

# Label para mostrar el resultado
label_resultado = ttk.Label(root, text="")
label_resultado.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

# Iniciar el bucle principal de la interfaz
root.mainloop()