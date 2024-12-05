import requests
from bs4 import BeautifulSoup
import json

def scrap_tarifas(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
      
    script_tag = soup.find("script", text=lambda t: t and "dataJSONArray" in t)
    
    if not script_tag:
        print("No se encontró la variable JSON en los scripts.")
        return []
    
    script_content = script_tag.string
    start_index = script_content.find("dataJSONArray = JSON.parse('") + len("dataJSONArray = JSON.parse('")
    end_index = script_content.find("');", start_index)
    json_data = script_content[start_index:end_index]

    data = json.loads(json_data)
    return data

def filtrar_tarifas(data, precio_min, precio_max):
    tarifas_filtradas = [
        item for item in data
        if precio_min <= float(item["PRECIO_MENSUAL"]) <= precio_max
    ]
    return tarifas_filtradas

# MAIN PARA PROBAR
if __name__ == "__main__":
    url = "https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasInternetFijo"
    data = scrap_tarifas(url)
    
    if data:
        precio_min = 500
        precio_max = 1450
        tarifas = filtrar_tarifas(data, precio_min, precio_max)

        with open("TarifasFiltradas.txt", "w") as file:
            for tarifa in tarifas:
                file.write(f"{tarifa['NOMBRE_COMERCIAL']} - {tarifa['PRECIO_MENSUAL']}\n")
        print(f"Se encontraron {len(tarifas)} tarifas en el rango de precios de: {precio_min} a: {precio_max}")
    else:
        print("No se encontraron tarifas.")
