import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

def scrape_news(start_date, end_date):
    base_url = "https://www.lostiempos.com/hemeroteca-fecha?fecha={}&page="
    
    # Abrir el archivo CSV para escribir
    with open("lostiempos.csv", mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["Fecha", "Título", "Sumario", "Enlace"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Escribir la cabecera del CSV
        writer.writeheader()

        current_date = start_date
        while current_date <= end_date:
            formatted_date = current_date.strftime("%d/%m/%Y")
            page = 0
            while True:
                # Construir la URL para la página actual
                url = base_url.format(formatted_date) + str(page)

                # Obtener el contenido de la página
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")

                # Encontrar todas las noticias en la estructura que mencionaste
                noticias = soup.select(".noticia-lt")

                # Si no hay noticias, salir del bucle
                if soup.select_one(".view-empty") or not noticias:
                    print(f"Ya no existen noticias para la fecha {formatted_date}.")
                    break

                for noticia in noticias:
                    fecha = noticia.select_one(".date-display-single")
                    titulo = noticia.select_one(".views-field-title a")
                    sumario = noticia.select_one(".views-field-field-noticia-sumario")

                    # Si se encuentra la fecha y el título, guarda la información en el CSV
                    if fecha and titulo:
                        writer.writerow(
                            {
                                "Fecha": fecha.text.strip(),
                                "Título": titulo.text.strip(),
                                "Sumario": sumario.text.strip() if sumario else "",
                                "Enlace": f"https://www.lostiempos.com{titulo['href']}",
                            }
                        )

                # Incrementar el número de página
                page += 1

            # Avanzar al siguiente día
            current_date += timedelta(days=1)

    messagebox.showinfo("Éxito", "Los datos han sido guardados en 'lostiempos.csv'.")

def start_scraping():
    try:
        start_date = datetime.strptime(start_date_entry.get(), "%d/%m/%Y")
        end_date = datetime.strptime(end_date_entry.get(), "%d/%m/%Y")
        if start_date > end_date:
            messagebox.showerror("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.")
            return
        scrape_news(start_date, end_date)
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha inválido. Usa DD/MM/YYYY.")

# Crear la ventana principal
root = tk.Tk()
root.title("Scraper de Noticias")

# Etiquetas y campos de entrada
tk.Label(root, text="Fecha de inicio (DD/MM/YYYY):").pack()
start_date_entry = tk.Entry(root)
start_date_entry.pack()

tk.Label(root, text="Fecha de fin (DD/MM/YYYY):").pack()
end_date_entry = tk.Entry(root)
end_date_entry.pack()

# Botón para iniciar el scraping
tk.Button(root, text="Iniciar Scraping", command=start_scraping).pack()

# Ejecutar la aplicación
root.mainloop()