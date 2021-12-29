from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTeg(url):
    
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    else:
        print(html)
    #try:
    #   bsObj = BeautifulSoup(html.read(), features="lxml")
     #   titel = bsObj.body.title
    #except AttributeError as e:
    #    return None
    #return titel

print("Старт!")
titel = getTeg("https://citeseerx.ist.psu.edu/search?q=mountaineering&submit.x=16&submit.y=15&sort=rlv&t=doc")
if titel == None:
    print("Titel could not be found")
else:
    print(titel)
