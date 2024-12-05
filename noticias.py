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

        news_data = []

        # Verificar qué fuentes están seleccionadas
        if los_tiempos_var.get():
            lostiempos = LosTiempos(start_date, end_date)
            news_data_lostiempos = lostiempos.scrape_news()
            news_data.extend(news_data_lostiempos)

        if el_deber_var.get():
            el_deber = ElDeber(start_date, end_date)
            news_data_el_deber = el_deber.obtener_todas_las_noticias()
            news_data.extend(news_data_el_deber)

        if opinion_var.get():
            opinion = Opinion(start_date, end_date)
            news_data_opinion = opinion.obtener_noticias_por_rango()
            news_data.extend(news_data_opinion)

        if not news_data:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna fuente de noticias.")
            return

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

# Variables para los checkbuttons
los_tiempos_var = tk.BooleanVar(value=True)  # Por defecto seleccionado
el_deber_var = tk.BooleanVar(value=True)      # Por defecto seleccionado
opinion_var = tk.BooleanVar(value=True)       # Por defecto seleccionado

# Checkbuttons para seleccionar fuentes
tk.Checkbutton(root, text="Los Tiempos", variable=los_tiempos_var).pack()
tk.Checkbutton(root, text="El Deber", variable=el_deber_var).pack()
tk.Checkbutton(root, text="Opinión", variable=opinion_var).pack()

# Botón para iniciar el scraping
tk.Button(root, text="Iniciar Scraping", command=start_scraping).pack()

# Ejecutar la aplicación
root.mainloop()