import json

with open('josn.backup/mountaineering.json') as f:
    x = json.load(f)

sRecords = x.get("records")
sPublisher = sRecords[0].get("record").get("publisher")[0]
sSurce = sRecords[0].get("record").get("source")
sLanguage = sRecords[0].get("record").get("language")
sYear = sRecords[0].get("record").get("publicationDate")
sTitel = sRecords[0].get("record").get("title")
sFirstAuthor = sRecords[0].get("record").get("creator")[0]
sSecondAuthor = sRecords[0].get("record").get("creator")[1]
sAbstract = sRecords[0].get("record").get("description")
lKeywords = sRecords[0].get("record").get("subjects")
sKeywords = ''
for sKeyword in lKeywords:
    print(sKeyword)
    sKeywords = sKeywords + ", " + sKeyword

sKeywords = str(sKeywords).lower()
sDOI = sRecords[0].get("record").get("url")
sURL = sRecords[0].get("record").get("allUrls")[1]

print("Publisher: " + str(sPublisher))
print("Surce: " + str(sSurce))
print("Language: " + str(sLanguage))
print("Year: " + str(sYear))
print("Titel: " + str(sTitel))
print("Author: " + str(sFirstAuthor))
print("Author: " + str(sSecondAuthor))
print("Abstract: " + str(sAbstract))
print("Keywords: " + str(sKeywords))
print("DOI: " + str(sDOI))
print("URL: " + str(sURL))
