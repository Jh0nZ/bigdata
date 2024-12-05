from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower, count
from pyspark.sql import functions as F

# Crear una sesión de Spark
spark = SparkSession.builder.appName("Obtener noticia más importante").getOrCreate()

# Cargar el archivo CSV
df = spark.read.csv(
    "hdfs:///datos/lostiempos.csv", header=True, inferSchema=True
)

# Mostrar el esquema del DataFrame
df.printSchema()

# Función para obtener la noticia más importante de una fecha específica
def obtener_noticia_mas_importante(fecha):
    # Filtrar por la fecha dada
    noticia_fecha = df.filter(col("Fecha") == fecha)
    # Unir el título y el sumario en una sola columna para el análisis
    noticia_fecha = noticia_fecha.withColumn(
        "texto_completo", F.concat_ws(" ", col("Título"), col("Sumario"))
    )
    # Dividir el texto en palabras, convertir a minúsculas y contar la frecuencia de cada palabra
    palabras = noticia_fecha.select(
        explode(split(lower(col("texto_completo")), " ")).alias("palabra")
    )
    # Contar la frecuencia de cada palabra
    frecuencia_palabras = palabras.groupBy("palabra").agg(
        count("palabra").alias("frecuencia")
    )
    # Obtener las palabras más frecuentes
    palabras_frecuentes = frecuencia_palabras.orderBy(desc("frecuencia")).limit(
        10
    )  # Cambia el límite según sea necesario
    # Recoger las palabras más frecuentes en una lista
    palabras_frecuentes_list = [row["palabra"] for row in palabras_frecuentes.collect()]
    # Filtrar las noticias que contienen la mayor cantidad de palabras frecuentes
    def contar_palabras_frecuentes(texto):
        return sum(
            1 for palabra in palabras_frecuentes_list if palabra in texto.lower()
        )
    contar_palabras_frecuentes_udf = F.udf(contar_palabras_frecuentes)
    # Añadir una columna con el conteo de palabras frecuentes
    noticia_fecha = noticia_fecha.withColumn(
        "conteo_palabras_frecuentes",
        contar_palabras_frecuentes_udf(col("texto_completo")),
    )

    # Obtener la noticia con el mayor conteo de palabras frecuentes

    noticia_mas_importante = noticia_fecha.orderBy(
        desc("conteo_palabras_frecuentes")
    ).first()

    return noticia_mas_importante


# Fecha de ejemplo

fecha_buscada = "25/11/2024"


# Obtener la noticia más importante

noticia = obtener_noticia_mas_importante(fecha_buscada)


# Mostrar la noticia más importante

if noticia:

    print(f"Fecha: {noticia['Fecha']}")

    print(f"Título: {noticia['Título']}")

    print(f"Sumario: {noticia['Sumario']}")

    print(f"Enlace: {noticia['Enlace']}")

else:

    print("No se encontró ninguna noticia para la fecha dada.")


# Detener la sesión de Spark

spark.stop()
