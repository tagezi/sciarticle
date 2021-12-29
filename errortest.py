from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTeg(url):
    
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        titel = bsObj.body.h1
    except AttributeError as e:
        return None
    return titel

titel = getTeg("https://virtualenv.pypa.io/en/latest/installation.html")
if titel == None:
    print("Titel could not be found")
else:
    print(titel)
