from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower, count, to_date, concat_ws
from pyspark.sql.types import StringType, DateType

# Crear sesión de Spark
spark = SparkSession.builder.appName("NoticiasImportantes").getOrCreate()

# Cargar el archivo CSV desde HDFS
df = spark.read.option("header", "true").csv("hdfs:///datos/noticias.csv")

df = df.withColumn("fecha", to_date(col("fecha"), "dd/MM/yyyy"))
# Asegurar que el campo 'fecha' sea del tipo DateType
df = df.withColumn("fecha", col("fecha").cast(DateType()))

# Filtrar por el rango de fechas deseado
fecha_inicio = "2024-12-01"
fecha_fin = "2024-12-03"
df_filtrado = df.filter((col("fecha") >= fecha_inicio) & (col("fecha") <= fecha_fin))

# Combinar el título y el sumario en una sola columna
df_combined = df_filtrado.withColumn("texto_completo", concat_ws(" ", col("titulo"), col("sumario")))

# Dividir el texto en palabras, convertir a minúsculas y contar la frecuencia
df_palabras = df_combined.select(explode(split(lower(col("texto_completo")), " ")).alias("palabra"))

# Contar la frecuencia de cada palabra
df_frecuencia = df_palabras.groupBy("palabra").agg(count("*").alias("frecuencia"))

# Encontrar la palabra más común
df_mas_comun = df_frecuencia.orderBy(col("frecuencia").desc()).limit(1)

# Mostrar la palabra más común
print("Palabra más común:")
df_mas_comun.show() 