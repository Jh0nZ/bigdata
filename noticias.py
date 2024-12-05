import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from LosTiempos import LosTiempos
from ElDeber import ElDeber
from Opinion import Opinion
import numpy as np

def save_to_csv(news_data):
    # Guardar las noticias en un archivo CSV
    with open("noticias.csv", mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["fecha", "titulo", "sumario", "enlace", "fuente"]
        writer = csv.writer(csv_file)

        # Escribir la cabecera del CSV
        writer.writerow(fieldnames)

        # Escribir las noticias
        for row in news_data:
            writer.writerow(row)

    messagebox.showinfo("Éxito", "Los datos han sido guardados en 'noticias.csv'.")

def start_scraping():
    try:
        start_date = datetime.strptime(start_date_entry.get(), "%d/%m/%Y")
        end_date = datetime.strptime(end_date_entry.get(), "%d/%m/%Y")
        if start_date > end_date:
            messagebox.showerror("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.")
            return

        # Crear instancia de Lostiempos y obtener las noticias
        lostiempos = LosTiempos(start_date, end_date)
        news_data_lostiempos  = lostiempos.scrape_news()
        
        el_deber = ElDeber(start_date, end_date)
        news_data_el_deber = el_deber.obtener_todas_las_noticias()
        
        opinion = Opinion(start_date, end_date)
        news_data_opinion = opinion.obtener_noticias_por_rango()
        
        news_data = np.concatenate((news_data_el_deber, news_data_lostiempos, news_data_opinion))

        # Guardar los resultados en CSV
        save_to_csv(news_data)

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
