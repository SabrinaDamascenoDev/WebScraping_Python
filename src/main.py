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

elements = scraped.findAll("article", class_="product_pod")

for itens in elements:
    print(itens.h3.a["title"])
#Pegar os precos que estao em uma tag p com a classe price_color
prices = scraped.findAll("p", class_="price_color")

for price in prices:
    # Tirar um element
    price = float(price.text.lstrip("£"))
    print(price)
    print(price)

results = []

for element in elements:
    results.append(element.h3.a['title'])

resultsPrice = []

for price in prices:
    price = float(price.text.lstrip("£"))
    resultsPrice.append(price)

print(list(zip(results, resultsPrice)))

resul = []
articles = scraped.findAll("article", class_="product_pod")

for article in articles:
    nome = article.h3.a['title']
    preco = article.find("div", class_="product_price").find("p", class_="price_color")
    preco = float(preco.text.lstrip("£"))
    dicDosDois = {nome: preco}
    resul.append(dicDosDois)

print(resul)

print(scraped.select(".product_price .price_color"))
