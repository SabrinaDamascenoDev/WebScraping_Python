import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os


load_dotenv()
link = os.getenv("EMAIL_USER") #Pega a variavel de ambiente
link_pass = os.getenv("EMAIL_PASS") #Pega a variavel de ambiente

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



print(nome_musicas)

#Entra no firefox usando o selenium
driver = webdriver.Firefox()
driver.maximize_window()

#Espera para aparecer elemento
wait = WebDriverWait(driver, 3)
presence = EC.presence_of_element_located
visible = EC.visibility_of_element_located

#Pesquisa
driver.get("https://www.youtube.com/")

#Clica no botao com esse href para fazer login no woutube, mas tem um timeout de 10 para esperar aparecer elemento
login_href = "https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dpt%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=pt-BR&ec=65620"
login_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f'//a[@href="{login_href}"]'))
)
login_link.click()

#Add email no input, mas antes espera aparecer o elemento
login_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'identifierId'))
)
login_input.send_keys(f"{link}")
login_input.send_keys(Keys.RETURN)

#Add pass no input mas antes espera aparecer o elemento
login_pass = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'Passwd'))
)
login_pass.send_keys(f"{link_pass}")
login_pass.send_keys(Keys.RETURN)







