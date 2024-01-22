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

chromeDriver = webdriver.Chrome()

chromeDriver.get("https://www.quepasaoaxaca.com/events-guide/")


try:
    getElembyLinkText = WebDriverWait(chromeDriver, 20).until(ExpectedCond.presence_of_element_located((By.CLASS_NAME, "evoet_title")))

    print(" El elemento si se encontró")
    element=chromeDriver.find_element("class name","evoet_title")
    print(element)
    print(getElembyLinkText)
    page = BeautifulSoup(chromeDriver.page_source,'html.parser')
    bloque = page.find('span',attrs={'class':'evoet_title'})
    print(bloque)

except TimeoutException:
    print ("El elemento no se mostró")
    chromeDriver.quit()



# element=driver.find_element("class name","evoet_title")
# print(element)

# soup =BeautifulSoup(chromeDriver.page_source,'lxml')
# titulo = soup.find('span',)


# ubicacion = ""

# driver = webdriver.Chrome()
# driver.implicitly_wait(80)

home_link = 'https://www.quepasaoaxaca.com/events-guide/'

# driver.get(home_link)
# page = bs4.BeautifulSoup(driver.page_source,'html.parser')

# print(page.prettify())

# element=driver.find_element("class name","evoet_title")
# print(element)
# for span in element :
#     print(span)

# spans = page.find_all('span')

# print(spans)

# for span in spans :
#     print(spans.get_text(strip=True))

#<span class="evoet_title evcal_desc2 evcal_event_title" itemprop="name">January Film Series</span>
