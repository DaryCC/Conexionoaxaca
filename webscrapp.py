import bs4 #solo para el chequeo
import requests

print("Version del bs4:" , bs4.__version__)
print("Version del requests:", requests.__version__)

URL_BASE = 'https://www.quepasaoaxaca.com/events-guide/'

pedido_obtenido = requests.get(URL_BASE,headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
"Accept-Encoding":"gzip, deflate",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT":"1"},cookies={"moove_gdpr_popup":"%7B%22strict%22%3A%221%22%2C%22thirdparty%22%3A%221%22%2C%22advanced%22%3A%221%22%7D"})

html_obtenido = pedido_obtenido.text
# print(html_obtenido)

soup = bs4.BeautifulSoup(html_obtenido, "html.parser")
# print(soup.prettify())
# print(soup)

# print(type(soup))
# h2 = soup.find('h1')
# print(h2.text)

# h2_todos = soup.find_all('h3')
# print(h2_todos)
# for todo in h2_todos:
    # print(todo.get_text(strip=True))

#Clase
spans = soup.find_all('span')

print(spans)

# for span in spans :
#     print(spans.get_text(strip=True))
