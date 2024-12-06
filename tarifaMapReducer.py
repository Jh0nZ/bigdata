from mrjob.job import MRJob

class MRTarifaMinima(MRJob):

    def mapper(self, _, line):
 
        # Suponiendo que la línea está separada por comas
        fields = line.split(',')
        if fields[0] == 'ID_TARIFA':
            return  # Skip this line
        departamento = fields[3]
        tipo_conexion = fields[12]
        plan_vigente = fields[13]
        precio_mensual = float(fields[10])
        nombre_comercial = fields[2]
        ancho_banda_bajada = fields[9]

        yield (departamento, tipo_conexion, plan_vigente), (precio_mensual, nombre_comercial, ancho_banda_bajada)

    def reducer(self, key, values):
        # Encontrar la tarifa mínima
        min_tarifa = min(values, key=lambda x: x[0])  # x[0] es el precio mensual
        yield key, min_tarifa

if __name__ == '__main__':
    MRTarifaMinima.run()