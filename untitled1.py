from bs4 import BeautifulSoup
import requests

url="http://books.toscrape.com/catalogue/page-1.html"
result =requests.get(url)


doc=BeautifulSoup(result.text,"html.parser")
print(doc.prettify())
tag=doc.find_all("h3")
parent=tag[0].parent
x=0
for a in doc.find_all("h3"):
    parent=tag[x].parent
    print(parent.find("img")["alt"])
    x=x+1
    
    
