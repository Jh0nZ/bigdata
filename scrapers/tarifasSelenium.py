from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Configura el driver (en este caso, Chrome)
driver = webdriver.Chrome()  # Asegúrate de que el ChromeDriver esté en tu PATH

# Abre la página web
driver.get('https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasInternetFijo')

# Espera a que la página cargue
time.sleep(5)  # Ajusta el tiempo según sea necesario

# Función para obtener los nombres de la cabecera
def obtener_nombres_cabecera():
    cabecera = driver.find_elements(By.CSS_SELECTOR, 'thead th')
    nombres = [celda.text for celda in cabecera]
    return nombres

# Función para obtener los datos de la tabla
def obtener_datos_tabla():
    datos_tabla = []
    filas = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, 'td')
        datos = [celda.text for celda in celdas]
        datos_tabla.append(datos)
    return datos_tabla

# Abre el archivo CSV para escribir
with open('tarifas.csv', mode='w', newline='', encoding='utf-8') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)

    # Escribe los nombres de la cabecera en el CSV
    nombres_cabecera = obtener_nombres_cabecera()
    escritor_csv.writerow(nombres_cabecera)

    # Escribe los datos de la primera página en el CSV
    datos_tabla = obtener_datos_tabla()
    for datos in datos_tabla:
        escritor_csv.writerow(datos)

    # Encuentra y haz clic en el botón para cargar más datos
    while True:
        try:
            boton_siguiente = driver.find_element(By.ID, 'kt_table_next')
            if 'disabled' in boton_siguiente.get_attribute('class'):
                print("El botón 'Siguiente' está deshabilitado. Deteniendo el scraping.")
                break
            boton_siguiente.click()
            #time.sleep(0.1)

            datos_tabla = obtener_datos_tabla()
            for datos in datos_tabla:
                escritor_csv.writerow(datos)
        except Exception as e:
            pass

# Cierra el navegador
driver.quit()