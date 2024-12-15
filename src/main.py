import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/index.html"
response = requests.get(url)
# Pegar o conteudo html da página
html = response.content
scraped = BeautifulSoup(html, "html.parser")
#Pega o titulo da página
print(scraped.title)

# Pega só o texto sem a tag <title>
print(scraped.title.text)
# Tira as strings 'invisiveis' do \n, tira o espaçamento da borda
print(scraped.title.text.strip())
#Devolve o primeiro elemento com a teg a
print(scraped.find("a").text.strip())
#Pegar um elemento que ta dentro da tag article com a classe product_podum a dentro de um h3
print(scraped.find("article", class_="product_pod").h3.a.text)

#Pega o nome td do livro pq ele ta dentro do atributo title da tag a
print(scraped.find("article", class_="product_pod").h3.a["title"])

