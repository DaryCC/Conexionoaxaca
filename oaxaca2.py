
from bs4 import BeautifulSoup
import bs4
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

chromeDriver = webdriver.Chrome()

chromeDriver.get("https://www.quepasaoaxaca.com/es/guia-de-eventos/")


try:
    getElembyLinkText = WebDriverWait(chromeDriver, 20).until(ExpectedCond.presence_of_element_located((By.CLASS_NAME, "evoday_events")))

    print(" El elemento si se encontró")

except TimeoutException:
    print ("El elemento no se mostró")
    chromeDriver.quit()



# element=chromeDriver.find_element("class name","evoet_title")
# print(element)
# print(getElembyLinkText)
page = BeautifulSoup(chromeDriver.page_source,'html.parser')
# print(page)

data = [
    json.loads(x.string) for x in page.find_all("script", type="application/ld+json")
]

# print(type(data))
today_date= datetime.now().strftime("%Y-%-m-%d")
#print(today_date)
# Create a regular expression pattern
pattern = re.compile(r"(\d{4}-\d{1,2}-\d{1,2})(T\d{2}:\d{2}-\d{1,2}:\d{2})?")



for evento in data:
    match = pattern.search(evento['startDate'])
    # print(evento['location'])

    if match :
        extracted_date = match.group(1)
        extracted_time = match.group(2)


        if today_date == extracted_date:

            print("===========================")

            try:
                evento['location']
                # print(evento['location'])
                print("Esto deberia de imprimir algo")
                for lugar in evento["location"]:
                    print(lugar['name'])
                    print(lugar['address']['streetAddress'])
            except KeyError:
                print('location is not available')

            evento['startDate']=today_date
            # print(f"Match found: {today_date} is equal to {extracted_date}")
            #clean name from '&quot'
            clean_name = evento['name'].replace("&quot;", "")
            evento["name"]=clean_name
            print(evento['name'])
            print(evento['startDate'])
            if extracted_time:
                # Parse the time string and format it
                # Create a regular expression pattern to extract the string between "T" and "-"
                between_pattern = re.compile(r"T([^-\s]+)-")
                between_match = between_pattern.search(extracted_time)

                print(between_match.group(1))
            else:
                print("")


            # print(evento['description'])
            # print(evento[])
