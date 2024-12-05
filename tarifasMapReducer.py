from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Iniciar una sesión de Spark
spark = SparkSession.builder.appName("TarifaMasBaja").getOrCreate()

# Cargar el archivo CSV en un DataFrame
df = spark.read.csv("hdfs:///datos/tarifas.csv", header=True, inferSchema=True)

# Filtrar por tipo de conexión y departamento (ciudad)
tipo_conexion = "FIBRA"  # Cambia según lo que necesites
ciudad = "Cochabamba"  # Cambia a la ciudad que buscas
df_filtrado = df.filter((df["Tipo de Conexión"] == tipo_conexion) & (df["Departamento"] == ciudad))

tarifa_minima = (
    df_filtrado
    .groupBy("Departamento", "Tipo de Conexión")
    .agg(
        F.min("Precio (Bs)").alias("Precio Minimo"),
    )
)

# Mostrar el resultado
tarifa_minima.show()
