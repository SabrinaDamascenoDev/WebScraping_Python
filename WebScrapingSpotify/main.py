import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time


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
login_pass = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.NAME, 'Passwd'))
)
login_pass.send_keys(f"{link_pass}")
login_pass.send_keys(Keys.RETURN)

# Clicar no input de pesquisa
pesquisa_musica = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.NAME, 'search_query'))
)
pesquisa_musica.click()

#Pesquisar nomes das musicas no youtube e criar a playlist quando for adicionar a primeira música
for musica in musicas_divs:
    #Verificar se o input de pesquisa esta vazio, se nao estiver deixa-lo
    pesquisa_musica = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.NAME, 'search_query'))
    )
    pesquisa_musica.clear()

    pesquisa_musica.send_keys(f"{musica.text.strip()}")
    pesquisa_musica.send_keys(Keys.RETURN)

    try:
        press_opitions = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="menu"]//button[contains(@aria-label, "Menu") and contains(@class, "style-scope yt-icon-button")]'))
        )
        press_opitions = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="menu"]//button[contains(@aria-label, "Menu") and contains(@class, "style-scope yt-icon-button")]'))
        )
        press_opitions.click()
    except TimeoutException:
         print("Erro: O botão não foi encontrado ou não estava clicável.")
    except Exception as err:
        print(f"Ocorre un erro: {err}")
    try:
        press_playlist = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'style-scope ytd-menu-service-item-renderer'))
        )
        if len(press_playlist) >= 3:
            press_playlist[2].click()

    except TimeoutError:
        print("Erro: O tempo limite foi excedido e os elementos não foram encontrados.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    #Se o index for 0, criar playlist
    if musicas_divs.index(musica) == 0:
        press_newPlatist = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Nova playlist"]'))
        )
        press_newPlatist.click()

        add_nome = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ytStandardsTextareaShapeTextarea'))
        )
        add_nome.send_keys(nome[:len(nome)-9])
        add_nome.send_keys(Keys.RETURN)

        try:
            #Clica em salvar
            buttons = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//button[@aria-label="Criar"]'))
            )
            if len(buttons) >= 2:
                press_create = buttons[1]
            press_create.click()
        except TimeoutException:
            print("Erro: O botão ou modal não ficaram disponíveis a tempo.")
        except Exception as err:
            print(f"Ocorre un erro: {err}")

        time.sleep(2)
    else:
        #Clicar na playlist com o mesmo nome da playlist do Spotify
        try:
            element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f'//yt-formatted-string[@aria-label="{nome[:len(nome)-9]}Particular"]'))
            )
            element.click()

        except TimeoutException:
            print("Erro: O elemento não ficou disponível a tempo.")
        except Exception as err:
            print(f"Ocorreu um erro: {err}")
        time.sleep(2)
