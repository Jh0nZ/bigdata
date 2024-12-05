import requests
import numpy as np
from datetime import datetime, timedelta

categories_map = {
    "La Paz": "la-paz",
    "Tenis": "tenis",
    "OEP": "oep",
    "Sociales": "sociales",
    "Opinión": "opinion",
    "Oriente Petrolero": "oriente-petrolero",
    "Para Ellas": "para-ellas",
    "Fuera De Juego": "fuera-de-juego",
    "Dinero": "dinero",
    "Royal Pari FC": "royal-pari-fc",
    "Real Santa Cruz": "real-santa-cruz",
    "Sucre": "sucre",
    "Santa Cruz": "santa-cruz",
    "Bolívar": "bolivar",
    "Motor": "motor",
    "PAÍS": "pais",
    "Fútbol": "futbol",
    "BBC": "bbc",
    "Blooming": "blooming",
    "Escenas": "escenas",
    "Edición Impresa": "edicion-impresa",
    "Gobernación": "gobernacion",
    "Mundo": "mundo",
    "GENTE": "gente",
    "Real Tomayapo": "real-tomayapo",
    "GeekED": "geeked",
    "Dw": "dw",
    "Oruro": "oruro",
    "Educación y sociedad": "educacion-y-sociedad",
    "Rfi": "rfi",
    "Multideportivo": "multideportivo",
    "Te Puede Interesar": "te-puede-interesar",
    "ECONOMÍA": "economia"
}

class ElDeber:
    def __init__(self, fecha_inicio, fecha_fin):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.todas_las_noticias = []

    def obtener_noticias(self, fecha):
        fecha_str = fecha.strftime("%d-%m-%Y")
        fecha_barras = fecha.strftime("%d/%m/%Y")
        base_url = f"https://eldeber.com.bo/api/news/getMoreLastNews?from={{}}&date={fecha_str}"
        noticias_dia = []
        from_param = 0
        while True:
            url = base_url.format(from_param)
            response = requests.get(url)
            if response.status_code == 200:
                noticias = response.json()
                if not noticias:
                    print(f"No hay más noticias disponibles para la fecha {fecha.strftime("%d-%m-%Y")} el deber.")
                    break
                for noticia in noticias:
                    noticias_dia.append(
                        [
                            fecha_barras,
                            noticia.get("Title_en"),
                            noticia.get("Description_en"),
                            f'https://eldeber.com.bo/{categories_map.get(noticia.get("Nodes_en", [None])[0], "")}/{noticia.get("Url")}_{noticia.get("Id")}',
                            "eldeber"
                        ]
                    )
                from_param += len(noticias)
            else:
                print(f"Error al obtener datos: {response.status_code}")
                break
        return noticias_dia

    def obtener_todas_las_noticias(self):
        print(f"Obteniendo noticias de el deber desde {self.fecha_inicio.strftime('%d/%m/%Y')} hasta {self.fecha_fin.strftime('%d/%m/%Y')}")
        fecha_actual = self.fecha_inicio
        while fecha_actual <= self.fecha_fin:
            noticias = self.obtener_noticias(fecha_actual)
            self.todas_las_noticias.extend(noticias)
            fecha_actual += timedelta(days=1)
        return np.array(self.todas_las_noticias)

# Ejemplo de uso
if __name__ == "__main__":
    el_deber = ElDeber(datetime.strptime("01/12/2024", "%d/%m/%Y"), datetime.strptime("01/12/2024", "%d/%m/%Y"))
    noticias_array = el_deber.obtener_todas_las_noticias()
    print("Noticias obtenidas:", noticias_array)