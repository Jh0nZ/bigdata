import requests
from bs4 import BeautifulSoup
import numpy as np
import time
from datetime import datetime, timedelta

class Opinion:
    def __init__(self, fecha_inicio, fecha_fin):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.base_url = "https://www.opinion.com.bo/archive/content"

    def obtener_noticias_por_fecha(self, fecha):
        pagina = 1
        noticias = []
        fecha_str = fecha.strftime("%Y/%m/%d")

        while True:
            url = f"{self.base_url}/{fecha_str}/?page={pagina}"
            response = requests.get(url)

            # Verificar que la solicitud fue exitosa
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Verificar si hay contenido disponible
                mensaje_no_contenido = soup.find('div', class_='message-inner', string="No hay contenidos disponibles.")
                if mensaje_no_contenido:
                    print(f"No hay más noticias disponibles para la fecha {fecha.strftime("%d-%m-%Y")} opinion.")
                    break  # Salir del bucle si no hay más contenidos

                # Encontrar todos los artículos
                for article in soup.find_all('article', class_='onm-new content image-top-left'):
                    titulo = article.find('h2', class_='title').get_text(strip=True)
                    sumario = article.find('div', class_='summary').get_text(strip=True)
                    enlace_completo = f"https://www.opinion.com.bo{article.find('a')['href']}"
                    noticias.append([fecha.strftime("%d-%m-%Y"), titulo, sumario, enlace_completo, "opinion"])
                pagina += 1
            else:
                print(f"Error al acceder al sitio web. Código de estado: {response.status_code}.")
                break

        return noticias

    def obtener_noticias_por_rango(self):
        print(f"Obteniendo noticias de Opinión desde {self.fecha_inicio.strftime('%d/%m/%Y')} hasta {self.fecha_fin.strftime('%d/%m/%Y')}")
        
        noticias_totales = []
        fecha_actual = self.fecha_inicio

        while fecha_actual <= self.fecha_fin:
            noticias = self.obtener_noticias_por_fecha(fecha_actual)
            noticias_totales.extend(noticias)
            fecha_actual += timedelta(days=1)

        return np.array(noticias_totales)

# Ejemplo de uso
if __name__ == "__main__":
    # Definir el rango de fechas
    fecha_inicio = datetime(2024, 12, 1)
    fecha_fin = datetime(2024, 12, 5)

    # Crear una instancia de la clase Opinion
    opinion = Opinion(fecha_inicio, fecha_fin)

    # Imprimir el array de noticias
    print(opinion.obtener_noticias_por_rango())