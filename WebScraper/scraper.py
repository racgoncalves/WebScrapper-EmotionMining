from bs4 import BeautifulSoup
import requests

html = requests.get("https://acontecebotucatu.com.br/").content

soup = BeautifulSoup(html, 'html.parser')

#print(soup.prettify())

#soup.find(id=”link3″)

teste = soup.find_all("h4", class_="entry-title")

botucatu = 0
for texto in teste:
    textos = texto.find("a")
    if(textos.string.find("Botucatu") != -1):
        botucatu += 1
    print(textos.string)

print("\n\n",botucatu,"\n\n")

teste2 = soup.find_all("p", class_="title")

pardini = 0
for texto in teste2:
    textos = texto.find("a")
    if(textos.string.find("Pardini") != -1):
        pardini += 1
    print(textos.string)

print("\n\n",pardini)


