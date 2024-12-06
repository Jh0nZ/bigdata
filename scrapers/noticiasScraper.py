import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from scrapers.LosTiempos import LosTiempos
from scrapers.ElDeber import ElDeber
from scrapers.Opinion import Opinion
import threading

# Lista para almacenar los resultados de las noticias
news_data = []

def save_to_csv(news_data):
    # Guardar las noticias en un archivo CSV
    with open("data/noticias.csv", mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["fecha", "titulo", "sumario", "enlace", "fuente"]
        writer = csv.writer(csv_file)

        # Escribir la cabecera del CSV
        writer.writerow(fieldnames)

        # Escribir las noticias
        for row in news_data:
            writer.writerow(row)

    messagebox.showinfo("Éxito", "Los datos han sido guardados en 'data/noticias.csv'.")

def scrape_los_tiempos(start_date, end_date):
    global news_data
    lostiempos = LosTiempos(start_date, end_date)
    news_data_lostiempos = lostiempos.scrape_news()
    news_data.extend(news_data_lostiempos)

def scrape_el_deber(start_date, end_date):
    global news_data
    el_deber = ElDeber(start_date, end_date)
    news_data_el_deber = el_deber.obtener_todas_las_noticias()
    news_data.extend(news_data_el_deber)

def scrape_opinion(start_date, end_date):
    global news_data
    opinion = Opinion(start_date, end_date)
    news_data_opinion = opinion.obtener_noticias_por_rango()
    news_data.extend(news_data_opinion)

def start_scraping():
    progress_bar.start()
    start_button.config(state=tk.DISABLED)  # Deshabilitar el botón

    try:
        start_date = datetime.strptime(start_date_entry.get(), "%d/%m/%Y")
        end_date = datetime.strptime(end_date_entry.get(), "%d/%m/%Y")
        if start_date > end_date:
            messagebox.showerror("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.")
            return

        threads = []

        # Verificar qué fuentes están seleccionadas y crear hilos
        if los_tiempos_var.get():
            thread = threading.Thread(target=scrape_los_tiempos, args=(start_date, end_date))
            threads.append(thread)
            thread.start()

        if el_deber_var.get():
            thread = threading.Thread(target=scrape_el_deber, args=(start_date, end_date))
            threads.append(thread)
            thread.start()

        if opinion_var.get():
            thread = threading.Thread(target=scrape_opinion, args=(start_date, end_date))
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

        if not news_data:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna fuente de noticias o no se encontraron resultados.")
            return

        # Guardar los resultados en CSV
        save_to_csv(news_data)

    except ValueError:
        messagebox.showerror("Error", "Formato de fecha inválido. Usa DD/MM/YYYY.")
    finally:
        # Detener el progreso y habilitar el botón
        progress_bar.stop()
        start_button.config(state=tk.NORMAL)

def start_scraping_thread():
    # Ejecutar la función de scraping en un hilo separado
    threading.Thread(target=start_scraping).start()

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

# Progressbar
progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.pack(pady=10)

# Botón para iniciar el scraping
start_button = tk.Button(root, text="Iniciar Scraping", command=start_scraping_thread)
start_button.pack()

# Ejecutar la aplicación
root.mainloop()