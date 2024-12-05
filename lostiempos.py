import requests
from bs4 import BeautifulSoup
import csv

# URL base de la página a scrapear
base_url = "https://www.lostiempos.com/hemeroteca-fecha?fecha=15/04/2024&page="

#21/04/2016 fecha prohibida

# Abrir el archivo CSV para escribir
with open("noticias.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["Fecha", "Título", "Sumario", "Enlace"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Escribir la cabecera del CSV
    writer.writeheader()

    page = 0
    while True:
        # Construir la URL para la página actual
        url = f"{base_url}{page}"

        # Obtener el contenido de la página
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Encontrar todas las noticias en la estructura que mencionaste
        noticias = soup.select(".noticia-lt")

        # Si no hay noticias, salir del bucle
        # Verificar si no hay noticias

        if soup.select_one(".view-empty") or soup.select_one(".views-field-title"):
            print("No existen noticias para esta fecha. Saliendo del bucle.")
            break

        for noticia in noticias:
            fecha = noticia.select_one(".date-display-single")
            titulo = noticia.select_one(".views-field-title a")
            sumario = noticia.select_one(".views-field-field-noticia-sumario")

            # Si se encuentra la fecha y el título, guarda la información en el CSV
            if fecha and titulo:
                writer.writerow(
                    {
                        "fecha": fecha.text.strip(),
                        "titulo": titulo.text.strip(),
                        "sumario": sumario.text.strip() if sumario else "",
                        "enlace": f"https://www.lostiempos.com{titulo['href']}",
                    }
                )

        # Incrementar el número de página
        page += 1

print("Los datos han sido guardados en 'noticias2.csv'.")
