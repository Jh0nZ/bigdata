from pyspark.sql import SparkSession

# Iniciar una sesión de Spark
spark = SparkSession.builder.appName("TarifaMasBaja").getOrCreate()

# Cargar el archivo CSV en un DataFrame
df = spark.read.csv("hdfs:///ruta/destino/tarifas.csv", header=True, inferSchema=True)

# Filtrar por tipo de conexión y departamento (ciudad)
tipo_conexion = "Fibra óptica"  # Cambia según lo que necesites
ciudad = "La Paz"  # Cambia a la ciudad que buscas

tarifa_minima = (
    df.filter((df["Tipo de Conexión"] == tipo_conexion) & (df["Departamento"] == ciudad))
    .groupBy("Tipo de Conexión", "Departamento")
    .min("Precio (Bs)")
)

# Mostrar el resultado
tarifa_minima.show()
