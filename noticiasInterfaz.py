import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, to_date, length, desc, lit
from datetime import datetime

# Crear sesión de Spark
spark = SparkSession.builder.appName("NoticiasImportantes").getOrCreate()

# Cargar el archivo CSV desde HDFS
df = spark.read.option("header", "true").csv("hdfs:///datos/noticias.csv")

# Convertir la columna 'fecha' al tipo DateType
df = df.withColumn("fecha", to_date(col("fecha"), "dd/MM/yyyy"))


def buscar_noticia():
    fecha_inicio = entry_fecha_inicio.get()
    fecha_fin = entry_fecha_fin.get()

    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")
        fecha_inicio_formateada = fecha_inicio_dt.strftime("%Y-%m-%d")
        fecha_fin_formateada = fecha_fin_dt.strftime("%Y-%m-%d")

        # Filtrar por el rango de fechas deseado
        df_filtrado = df.filter(
            (col("fecha") >= lit(fecha_inicio_formateada))
            & (col("fecha") <= lit(fecha_fin_formateada))
        )

        # Combinar el título y el sumario en una sola columna
        df_combined = df_filtrado.withColumn(
            "texto_completo", concat_ws(" ", col("titulo"), col("sumario"))
        )

        # Calcular una métrica de relevancia (ejemplo: longitud del texto completo)
        df_relevancia = df_combined.withColumn(
            "relevancia", length(col("texto_completo"))
        )

        # Ordenar por la métrica de relevancia en orden descendente
        df_ordenado = df_relevancia.orderBy(desc("relevancia"))

        # Seleccionar la noticia más relevante
        noticia_mas_relevante = df_ordenado.limit(1)

        # Obtener los resultados
        resultado = noticia_mas_relevante.select(
            "fecha", "titulo", "sumario", "enlace", "fuente", "relevancia"
        ).collect()

        if resultado:
            noticia = resultado[0]
            mensaje = f"Fecha: {noticia['fecha']}\nTítulo: {noticia['titulo']}\nSumario: {noticia['sumario']}\nEnlace: {noticia['enlace']}\nFuente: {noticia['fuente']}\nRelevancia: {noticia['relevancia']}"
            messagebox.showinfo("Noticia más relevante", mensaje)
        else:
            messagebox.showwarning(
                "Sin resultados",
                "No se encontraron noticias en el rango de fechas especificado.",
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Crear la ventana principal
root = tk.Tk()
root.title("Buscador de Noticias")

# Etiquetas y campos de entrada
label_fecha_inicio = tk.Label(root, text="Fecha Inicio (dd/MM/yyyy):")
label_fecha_inicio.pack()

entry_fecha_inicio = tk.Entry(root)
entry_fecha_inicio.pack()

label_fecha_fin = tk.Label(root, text="Fecha Fin (dd/MM/yyyy):")
label_fecha_fin.pack()

entry_fecha_fin = tk.Entry(root)
entry_fecha_fin.pack()

# Botón de búsqueda
boton_buscar = tk.Button(root, text="Buscar Noticia", command=buscar_noticia)
boton_buscar.pack()

# Iniciar el bucle de la interfaz gráfica
root.mainloop()
