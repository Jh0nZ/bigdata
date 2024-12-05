import tkinter as tk
from tkinter import ttk
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Iniciar una sesión de Spark
spark = SparkSession.builder.appName("TarifaMasBaja").getOrCreate()

# Cargar el archivo CSV en un DataFrame
df = spark.read.csv("hdfs:///ruta/destino/tarifas.csv", header=True, inferSchema=True)

# Obtener los departamentos y tipos de conexión únicos
departamentos = df.select("Departamento").distinct().rdd.flatMap(lambda x: x).collect()
tipos_conexion = df.select("Tipo de Conexión").distinct().rdd.flatMap(lambda x: x).collect()

# Función para mostrar la tarifa mínima
def mostrar_tarifa():
    tipo_conexion = tipo_conexion_var.get()
    ciudad = ciudad_var.get()
    
    df_filtrado = df.filter((df["Tipo de Conexión"] == tipo_conexion) & (df["Departamento"] == ciudad))
    
    tarifa_minima = (
        df_filtrado
        .groupBy("Departamento", "Tipo de Conexión")
        .agg(
            F.min("Precio (Bs)").alias("Precio Minimo"),
        )
    )
    
    resultado = tarifa_minima.collect()
    
    if resultado:
        label_resultado.config(text=f"Precio Mínimo en {ciudad} ({tipo_conexion}): {resultado[0]['Precio Minimo']} Bs")
    else:
        label_resultado.config(text="No se encontraron tarifas.")

# Crear la ventana principal
root = tk.Tk()
root.title("Consulta de Tarifas")

# Variables para los selectores
ciudad_var = tk.StringVar()
tipo_conexion_var = tk.StringVar()

# Crear los selectores
ttk.Label(root, text="Selecciona un Departamento:").grid(column=0, row=0, padx=10, pady=10)
ciudad_combobox = ttk.Combobox(root, textvariable=ciudad_var, values=departamentos)
ciudad_combobox.grid(column=1, row=0, padx=10, pady=10)

ttk.Label(root, text="Selecciona un Tipo de Conexión:").grid(column=0, row=1, padx=10, pady=10)
tipo_combobox = ttk.Combobox(root, textvariable=tipo_conexion_var, values=tipos_conexion)
tipo_combobox.grid(column=1, row=1, padx=10, pady=10)

# Botón para mostrar el resultado
boton_mostrar = ttk.Button(root, text="Mostrar Tarifa Mínima", command=mostrar_tarifa)
boton_mostrar.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

# Label para mostrar el resultado
label_resultado = ttk.Label(root, text="")
label_resultado.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

# Iniciar el bucle principal de la interfaz
root.mainloop()