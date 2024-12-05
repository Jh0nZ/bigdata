import requests
import csv

fecha = "03-12-2024"
base_url = f"https://eldeber.com.bo/api/news/getMoreLastNews?from={{}}&date={fecha}"

with open("noticias_deber.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    fieldnames = [
        "fecha",
        "titulo",
        "sumario",
        "LastModificationDate",
        "Id",
        "PublicationDate",
        "Url",
        "Nodes_en",
        "AuthorName",
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Escribir la cabecera del CSV
    writer.writeheader()

    from_param = 0
    while True:
        url = base_url.format(from_param)

        response = requests.get(url)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            noticias = response.json()

            if not noticias:
                print("No hay más noticias para esta fecha. Saliendo del bucle.")
                break

            for noticia in noticias:
                writer.writerow(
                    {
                        "fecha": "03-12-2024",
                        "titulo": noticia.get("Title_en"),
                        "sumario": noticia.get("Description_en"),
                        "LastModificationDate": noticia.get("LastModificationDate"),
                        "Id": noticia.get("Id"),
                        "PublicationDate": noticia.get("PublicationDate"),
                        "Url": noticia.get("Url"),
                        "Nodes_en": ", ".join(noticia.get("Nodes_en", [])),
                        "AuthorName": ", ".join(noticia.get("AuthorName", [])),
                    }
                )
            from_param += len(noticias)

        else:
            print(f"Error al obtener datos: {response.status_code}")
            break

print("Los datos han sido guardados en 'noticias_deber.csv'.")
