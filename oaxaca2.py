from bs4 import BeautifulSoup
from urllib.parse import urlparse
import bs4
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
import pandas as pd
from datetime import date
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ExpectedCond
import json
import re
from datetime import datetime
import csv
import requests
import pywhatkit as kit
import tkinter as Tkinter
from unidecode import unidecode


chromeDriver = webdriver.Chrome()



chromeDriver.get("https://www.quepasaoaxaca.com/es/guia-de-eventos/")


try:
    getElembyLinkText = WebDriverWait(chromeDriver, 20).until(ExpectedCond.presence_of_element_located((By.CLASS_NAME, "eventon_desc_in")))
    # getElembyLinkText = WebDriverWait(chromeDriver, 20).until(ExpectedCond.presence_of_element_located((By.CLASS_NAME, "evoday_events")))
    print(" El elemento si se encontró")

except TimeoutException:
    print ("El elemento no se mostró")
    chromeDriver.quit()


page = BeautifulSoup(chromeDriver.page_source,'html.parser')
# print(page)
# print(page.find_all("script", type="application/ld+json"))
data=[]
for x in page.find_all('script', type="application/ld+json"):
    try:
        json_data = json.loads(x.string)
        data.append(json_data)
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        print(f"Contenido del JSON problemático: {x.string}")

#obtemos todos la información necesaria en  script/json
# data = [
#     json.loads(x.string) for x in page.find_all('script', type="application/ld+json")
# ]
# print(data)

# Extraer la fecha en el formato yyyy-m-d sin ceros a la izquierda
today_date = datetime.now().strftime("%Y-%-m-%-d")
#para windows es así
# now = datetime.now()
# today_date = f"{now.year}-{now.month}-{now.day}"

print(today_date)
# today_date=('2024-8-27')




# Create a regular expression pattern para extrer las fechas, excluyendo la hora
pattern = re.compile(r"(\d{4}-\d{1,2}-\d{1,2})(T\d{2}:\d{2}-\d{1,2}:\d{2})?")

nombre_evento =[]
fecha_evento=[]
hora_evento=[]
lugar_evento=[]
direccion_evento=[]
flyer_evento=[]

for evento in data:
    match = pattern.search(evento['startDate'])
    # print(evento['location'])

    if match :
        print('si hay eventos de este día')
        extracted_date = match.group(1)
        extracted_time = match.group(2)
        print('fecha extraida de pagina')
        print(extracted_date)
        # print('fecha de hoy sys')
        # print(today_date)
        # print('hora de hoy')
        # print(extracted_time)
        if today_date == extracted_date:

            print("===========================")

            evento['startDate']=today_date
            # print(f"Match found: {today_date} is equal to {extracted_date}")
            #clean name from '&quot'
            clean_name = evento['name'].replace("&quot;", "")
            evento["name"]=clean_name

            print(evento['name'])
            print(evento['startDate'])

            if evento['name']:
                nombre_evento.append(evento['name'])
            else: nombre_evento.append('')


            if evento['startDate']:
                fecha_evento.append(evento['startDate'])
            else: fecha_evento.append('')


            if extracted_time:

                # Create a regular expression pattern to extract the string between "T" and "-"
                between_pattern = re.compile(r"T([^-\s]+)-")
                between_match = between_pattern.search(extracted_time)

                print(between_match.group(1))
                hora_evento.append(between_match.group(1))
            else:
                print("")
                hora_evento.append('')


            try:
                evento['location']
                # print(evento['location'])
                # print("Esto deberia de imprimir algo")
                for lugar in evento["location"]:
                    print(lugar['name'])
                    lugar_evento.append(lugar['name'])
                    print(lugar['address']['streetAddress'])
                    direccion_evento.append(lugar['address']['streetAddress'])
            except KeyError:
                print('')
                lugar_evento.append('')
                direccion_evento.append('')

            imagen_input = evento['description']
            link_imagen = BeautifulSoup(imagen_input,'html.parser')
            print(link_imagen)
            if len(link_imagen)> 1 :
                print(len(link_imagen))
                print('si paso la condicion y no tiene informacion')
                img_url= link_imagen.find('img')['src']
                if img_url:
                    flyer_evento.append(img_url)
                else:
                    flyer_evento.append('')
                print(img_url)

            # print(evento['description'])
            # print(evento[])

#crear data frame en pandas
eventos_del_dia =  pd.DataFrame({

    "evento":nombre_evento,
    'fecha':fecha_evento,
    'hora':hora_evento,
    'lugar':lugar_evento,
    "direccion":direccion_evento,
    'url_of_the_image':flyer_evento,
})

print(eventos_del_dia)

cwd = os.getcwd()
path = cwd +"/eventos.csv"
eventos_del_dia.to_csv(path,index=False,header=True,encoding='utf-8-sig',index_label='index_imagen')



def download_images_from_csv(csv_file='eventos.csv', download_folder='images'):
    # Read data from CSV file
    df = pd.read_csv(csv_file)

    # Create the download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    # Iterate through each row in the CSV file
    for index, row in df.iterrows():
        # Get the URL of the image from the "url_of_the_image" column
        image_url = row['url_of_the_image']
        print(image_url)
        # Ensure the URL is not empty
        if pd.notna(image_url) and isinstance(image_url, str):
            # Get the file extension from the URL
            file_extension = os.path.splitext(urlparse(image_url).path)[1]

            # Construct the filename using the index from the CSV file
            filename = f"{download_folder}/image_{index}{file_extension}"

            # Download the image and save it with the constructed filename
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    file.write(response.content)
                print(f"Image {index} downloaded: {filename}")
            else:
                print(f"Failed to download image {index} from {image_url}")
        else:
            print(f"Skipping row {index} due to missing or invalid image URL")

# Example usage
download_images_from_csv(csv_file='eventos.csv', download_folder='images')

def remove_accents(csv_file):
    # Read data from CSV file
    df = pd.read_csv(csv_file)

    # Specify columns with 'object' data type to convert to string
    columns_to_convert = ['evento', 'fecha', 'hora', 'lugar', 'direccion','url_of_the_image']

    # Convert specified columns to string and remove accents
    for col in columns_to_convert:
        df[col] = df[col].astype(str).apply(unidecode)

    # Save the modified DataFrame to a new CSV file or update the existing one
    df.to_csv('modified_file.csv', index=False)

# Example usage
csv_file_path = 'your_file.csv'  # Replace with the actual path to your CSV file
remove_accents('eventos.csv')


# para enviar a grupos de whatsapp

#istala tkinter para linux o windows?, solo importa la librería
# import tkinter as Tkinter
#en arch sudo pacman -S tk

def post_event_to_whatsapp(csv_file='eventos.csv', images_folder='images'):
    # Read data from CSV file import tkinter as Tkinter
    print("*****************************************************")
    df = pd.read_csv(csv_file)
    print(df.dtypes)
    kit.sendwhatmsg_to_group_instantly("GNMmyHAdwSgElxJtecDgQo", "Para mas detalles consulta \n www.oaxacaevents.com  \n www.quepasaoaxaca.com \n automated by @luditalk")
    time.sleep(20)
    # Iterate through each row in the CSV file
    for _, row in df.iterrows():
        # Format the message

        for key in row:
            print(key)
            if key=='nan':
                row[key]=''

        # message = f"Evento: {row['evento']}\nFecha: {row['fecha']}\nHora: {row['hora']}\nLugar: {row['lugar']}\nDireccion: {row['direccion']}"
        message = f"Evento: {row['evento']}\nHora: {row['hora']}\nLugar: {row['lugar']}"

        # Find the image path
        image_index = row.name
        image_path = None

        for ext in ['jpg', 'jpeg', 'png']:
            potential_image_path = os.path.join(images_folder, f"image_{image_index}.{ext}")
            if os.path.exists(potential_image_path):
                image_path = potential_image_path
                break

        if image_path is None:
            print(f"Image not found for event {image_index}")
            continue
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(" ok si funciona hasta antes de enviar imagen")
        # Send the message with the image to WhatsApp group
        # kit.sendwhats_image("Posada 2016", image_path, message)
        # I0QVhEjPeNu1D11Yn6U86f
        # test buddy system
        #diversión GNMmyHAdwSgElxJtecDgQo
        #diversioón
        kit.sendwhats_image("GNMmyHAdwSgElxJtecDgQo",image_path,message,20,True,20)
        #posada
        # kit.sendwhats_image("LpGg58gwpTPKGhoUOfwHtP",image_path,message,20,True, 5)


# Example usage
post_event_to_whatsapp(csv_file='modified_file.csv', images_folder='images')



