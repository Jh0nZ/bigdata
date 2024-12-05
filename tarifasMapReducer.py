from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Iniciar una sesión de Spark
spark = SparkSession.builder.appName("TarifaMasBaja").getOrCreate()

# Cargar el archivo CSV en un DataFrame
df = spark.read.csv("hdfs:///ruta/destino/tarifas.csv", header=True, inferSchema=True)

# Filtrar por tipo de conexión y departamento (ciudad)
tipo_conexion = "FIBRA"  # Cambia según lo que necesites
ciudad = "Cochabamba"  # Cambia a la ciudad que buscas

tarifa_minima = (
    df.filter(df["Tipo de Conexión"] == tipo_conexion)
    .groupBy("Departamento", "Tipo de Conexión")
    .agg(
        F.min("Precio (Bs)").alias("Precio Minimo"),
        F.max("Velocidad Bajada (Mbps)").alias("Velocidad Maxima (Mbps)")
    )
)

# Mostrar el resultado
tarifa_minima.show()

# Filtrar el DataFrame por tipo de conexión y departamento

df_filtrado = df.filter((df["Tipo de Conexión"] == tipo_conexion) & (df["Departamento"] == ciudad))


# Ordenar por velocidad de bajada y obtener el precio más bajo

resultado = (
    df_filtrado.orderBy(df["Velocidad Bajada (Mbps)"].desc())
    .groupBy("Velocidad Bajada (Mbps)")
    .agg(F.min("Precio (Bs)").alias("Precio Minimo"))
    .sort("Velocidad Bajada (Mbps)")
)
# Mostrar el resultado
resultado.show()