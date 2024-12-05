import tkinter as tk
from tkinter import ttk, scrolledtext
from pyspark import SparkContext
from pyspark.sql import SparkSession

# Inicializa Spark
spark = SparkSession.builder \
    .appName("Contar palabras") \
    .getOrCreate()

# Crea un contexto de Spark
sc = spark.sparkContext

# Función para contar palabras
def contar_palabras():
    # Obtener los valores de entrada
    longitud_minima = int(longitud_minima_var.get())
    num_resultados = int(num_resultados_var.get())
    
    # Carga el archivo de texto
    archivo_texto = "hdfs:///datos/pg74840.txt"  # Cambia esto por la ruta de tu archivo
    texto_rdd = sc.textFile(archivo_texto)

    # Divide las líneas en palabras, convierte a minúsculas y filtra palabras vacías y de longitud menor o igual a longitud_minima
    palabras_rdd = texto_rdd.flatMap(lambda linea: linea.lower().split()) \
                            .filter(lambda palabra: palabra.isalpha() and len(palabra) >= longitud_minima)

    # Cuenta las palabras
    conteo_palabras_rdd = palabras_rdd.map(lambda palabra: (palabra, 1)) \
                                        .reduceByKey(lambda a, b: a + b)

    # Obtiene las palabras más comunes según el número solicitado
    top_palabras = conteo_palabras_rdd.takeOrdered(num_resultados, key=lambda x: -x[1])

    # Limpiar el área de texto
    area_texto.delete(1.0, tk.END)

    # Mostrar los resultados en el área de texto
    for palabra, conteo in top_palabras:
        area_texto.insert(tk.END, f"{palabra}: {conteo}\n")

# Crear la ventana principal
root = tk.Tk()
root.title("Contador de Palabras")

# Variables para los selectores
longitud_minima_var = tk.StringVar()
num_resultados_var = tk.StringVar()

# Crear los selectores
ttk.Label(root, text="Longitud mínima de palabras:").grid(column=0, row=0, padx=10, pady=10)
longitud_minima_entry = ttk.Entry(root, textvariable=longitud_minima_var)
longitud_minima_entry.grid(column=1, row=0, padx=10, pady=10)

ttk.Label(root, text="Número de resultados a mostrar:").grid(column=0, row=1, padx=10, pady=10)
num_resultados_entry = ttk.Entry(root, textvariable=num_resultados_var)
num_resultados_entry.grid(column=1, row=1, padx=10, pady=10)

# Botón para contar palabras
boton_contar = ttk.Button(root, text="Contar Palabras", command=contar_palabras)
boton_contar.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

# Área de texto desplazable para mostrar resultados
area_texto = scrolledtext.ScrolledText(root, width=50, height=15)
area_texto.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

# Iniciar el bucle principal de la interfaz
root.mainloop()

# Detiene el contexto de Spark al cerrar la aplicación
sc.stop()