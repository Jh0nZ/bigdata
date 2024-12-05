from pyspark import SparkContext
from pyspark.sql import SparkSession

# Inicializa Spark
spark = SparkSession.builder \
    .appName("Contar palabras") \
    .getOrCreate()

# Crea un contexto de Spark
sc = spark.sparkContext

# Carga el archivo de texto
archivo_texto = "txt/pg74840.txt"  # Cambia esto por la ruta de tu archivo
texto_rdd = sc.textFile(archivo_texto)

# Divide las líneas en palabras, convierte a minúsculas y filtra palabras vacías
palabras_rdd = texto_rdd.flatMap(lambda linea: linea.lower().split()) \
                        .filter(lambda palabra: palabra.isalpha())

# Cuenta las palabras
conteo_palabras_rdd = palabras_rdd.map(lambda palabra: (palabra, 1)) \
                                    .reduceByKey(lambda a, b: a + b)

# Obtiene las 3 palabras más comunes
top_3_palabras = conteo_palabras_rdd.takeOrdered(3, key=lambda x: -x[1])

# Muestra el resultado
for palabra, conteo in top_3_palabras:
    print(f"{palabra}: {conteo}")

# Detiene el contexto de Spark
sc.stop()