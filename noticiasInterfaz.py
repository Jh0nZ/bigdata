import tkinter as tk
from tkinter import Toplevel
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, to_date, length, desc, lit
from datetime import datetime
from tkinter import messagebox
# Crear sesión de Spark
spark = SparkSession.builder.appName("NoticiasImportantes").getOrCreate()

# Cargar el archivo CSV desde HDFS
df = spark.read.option("header", "true").csv("hdfs:///datos/noticias.csv")

# Convertir la columna 'fecha' al tipo DateType
df = df.withColumn("fecha", to_date(col("fecha"), "dd/MM/yyyy"))


def mostrar_noticia(noticia):
    """Crear una ventana personalizada para mostrar la noticia más relevante."""
    ventana = Toplevel(root)
    ventana.title("Noticia Más Relevante")
    
    # Configurar el tamaño de la ventana
    ventana.geometry("400x300")
    
    # Mostrar el mensaje
    texto = f"""
    Fecha: {noticia['fecha']}
    Título: {noticia['titulo']}
    Sumario: {noticia['sumario']}
    Enlace: {noticia['enlace']}
    Fuente: {noticia['fuente']}
    Relevancia: {noticia['relevancia']}
    """
    label_mensaje = tk.Label(ventana, text=texto, justify="left", anchor="w")
    label_mensaje.pack(pady=10, padx=10, fill="both")

    # Botón para copiar el enlace
    boton_copiar = tk.Button(
        ventana,
        text="Copiar Enlace",
        command=lambda: root.clipboard_clear() or root.clipboard_append(noticia['enlace'])
    )
    boton_copiar.pack(pady=10)

    # Botón para cerrar la ventana
    boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
    boton_cerrar.pack(pady=5)


def buscar_noticia():
    """Buscar y mostrar la noticia más relevante según el rango de fechas."""
    fecha_inicio = entry_fecha_inicio.get()
    fecha_fin = entry_fecha_fin.get()

    try:
        # Validar y formatear las fechas
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
            mostrar_noticia(noticia)
        else:
            messagebox.showwarning(
                "Sin Resultados",
                "No se encontraron noticias en el rango de fechas especificado.",
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Crear la ventana principal
root = tk.Tk()
root.title("Buscador de Noticias")
root.geometry("300x200")

# Etiquetas y campos de entrada
frame = tk.Frame(root, pady=10)
frame.pack(fill="both", expand=True)

label_fecha_inicio = tk.Label(frame, text="Fecha Inicio (dd/MM/yyyy):")
label_fecha_inicio.grid(row=0, column=0, sticky="w", padx=5, pady=5)

entry_fecha_inicio = tk.Entry(frame)
entry_fecha_inicio.grid(row=0, column=1, padx=5, pady=5)

label_fecha_fin = tk.Label(frame, text="Fecha Fin (dd/MM/yyyy):")
label_fecha_fin.grid(row=1, column=0, sticky="w", padx=5, pady=5)

entry_fecha_fin = tk.Entry(frame)
entry_fecha_fin.grid(row=1, column=1, padx=5, pady=5)

# Botón de búsqueda
boton_buscar = tk.Button(root, text="Buscar Noticia", command=buscar_noticia)
boton_buscar.pack(pady=10)

# Iniciar el bucle de la interfaz gráfica
root.mainloop()
