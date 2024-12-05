import requests
from bs4 import BeautifulSoup
import numpy as np
from datetime import timedelta

class LosTiempos:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.base_url = "https://www.lostiempos.com/hemeroteca-fecha?fecha={}&page="

    def scrape_news(self):
        print(f"Obteniendo noticias de Los Tiempos desde {self.start_date.strftime('%d/%m/%Y')} hasta {self.end_date.strftime('%d/%m/%Y')}")
        news_data = []

        current_date = self.start_date
        while current_date <= self.end_date:
            formatted_date = current_date.strftime("%m/%d/%Y").replace("/", "%2F")
            page = 0
            while True:
                # Construir la URL para la página actual
                url = self.base_url.format(formatted_date) + str(page)

                # Obtener el contenido de la página
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")

                # Encontrar todas las noticias en la estructura que mencionaste
                noticias = soup.select(".noticia-lt")

                # Si no hay noticias, salir del bucle
                if soup.select_one(".view-empty") or not noticias:
                    print(f"Ya no existen noticias para la fecha {current_date.strftime("%m/%d/%Y")} los tiempos.")
                    break

                for noticia in noticias:
                    fecha = noticia.select_one(".date-display-single")
                    titulo = noticia.select_one(".views-field-title a")
                    sumario = noticia.select_one(".views-field-field-noticia-sumario")
                    # Si se encuentra la fecha y el título, guarda la información
                    if fecha and titulo:
                        news_data.append(
                            [
                                fecha.text.strip(),
                                titulo.text.strip(),
                                sumario.text.strip() if sumario else "",
                                f"https://www.lostiempos.com{titulo['href']}",
                                "lostiempos"
                            ]
                        )

                # Incrementar el número de página
                page += 1

            # Avanzar al siguiente día
            current_date += timedelta(days=1)

        return np.array(news_data)
