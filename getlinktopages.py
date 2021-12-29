from urllib.request import urlopen
from bs4 import BeautifulSoup
import time


def collect_links(sURL):
    sHTML = urlopen(sURL)
    bsObj = BeautifulSoup(sHTML, "lxml")
    lListURl = bsObj.find("div", {"id": "mw-pages"}).findAll("a")

    for URL in lListURl:
        if URL.get_text() == "next page":
            sURL = "https://en.wikipedia.org" + URL.attrs['href']
            f.write(sURL + '\n')
            print(sURL)
            time.sleep(5)
            collect_links(sURL)
            return

    return


f = open('wikilinks.txt', 'w')
sURL = "https://en.wikipedia.org/w/index.php?title=Category:English-language_journals&pagefrom=African+Journal+of+Traditional%2C+Complementary+and+Alternative+Medicines#mw-pages"
html = urlopen(sURL)
f.write(sURL + '\n')

bsObj = BeautifulSoup(html, "lxml")
lListURl = bsObj.find("div", {"id": "mw-pages"}).findAll("a")

for URL in lListURl:
    if URL.get_text() == "next page":
        sURL = "https://en.wikipedia.org" + URL.attrs['href']
        f.write(sURL + '\n')
        time.sleep(5)
        print(sURL)
        collect_links(sURL)

f.close()
