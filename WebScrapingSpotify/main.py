import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#Pede a url do cliente e guarda na variavel response
url = input("Enter the Spotify Playlist URL: ")
response = requests.get(url)

#Pega o HTMl da url
html = response.text
soup = BeautifulSoup(html, 'html.parser')

#Pega o nome da playlist
nome = soup.title.text

nome_musicas = []
#Pega os nomes das músicas
musicas_divs = soup.find_all("div", class_="Areas__InteractiveArea-sc-8gfrea-0 Areas__Column-sc-8gfrea-5 bJSfgC jwUvtM")

for music in musicas_divs:
    musica = music.find("p", class_="encore-text encore-text-body-medium ListRowTitle__ListRowText-sc-1xe2if1-1 eFGzcP")
    if musica:
        nome_musicas.append(musica.text.strip()) #Guarda dentro de uma lista o nome da música






