from mrjob.job import MRJob

class MRTarifaMinima(MRJob):

    def mapper(self, _, line):
        # Suponiendo que la línea está separada por comas
        fields = line.split(',')
        departamento = fields[0]
        tipo_conexion = fields[1]
        plan_vigente = fields[2]
        precio_mensual = float(fields[3])
        nombre_comercial = fields[4]
        ancho_banda_bajada = fields[5]

        # Emitir solo si el plan vigente es "SI" o "NO"
        if plan_vigente in ["SI", "NO"]:
            yield (departamento, tipo_conexion, plan_vigente), (precio_mensual, nombre_comercial, ancho_banda_bajada)

    def reducer(self, key, values):
        # Encontrar la tarifa mínima
        min_tarifa = min(values, key=lambda x: x[0])  # x[0] es el precio mensual
        yield key, min_tarifa

if __name__ == '__main__':
    MRTarifaMinima.run()