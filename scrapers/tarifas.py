import requests
from bs4 import BeautifulSoup
import json
import csv

def scrap_tarifas(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Buscar el script que contiene "dataJSONArray"
    script_tag = soup.find("script", text=lambda t: t and "dataJSONArray" in t)
    if not script_tag:
        print("No se encontró la variable JSON en los scripts.")
        return []

    script_content = script_tag.string
    start_index = script_content.find("dataJSONArray = JSON.parse('") + len(
        "dataJSONArray = JSON.parse('"
    )
    end_index = script_content.find("');", start_index)

    json_data = script_content[start_index:end_index]

    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return []

    return data


def guardar_como_csv(data, filename="data/tarifas.csv"):
    if not data:
        print("No hay datos para guardar.")
        return

    # Extraer encabezados del primer elemento
    headers = data[0].keys()

    # Guardar datos en formato CSV
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"Datos guardados en {filename}")


if __name__ == "__main__":
    url = "https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasInternetFijo"
    data = scrap_tarifas(url)

    if data:
        print(f"Se han obtenido {len(data)} tarifas.")
        guardar_como_csv(data)
