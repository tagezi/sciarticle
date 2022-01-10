#     This code is a part of program Science Articles Orderliness
#     Copyright (C) 2021  Valerii Goncharuk (aka tagezi)
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json

with open('files/josn.backup/mountaineering.json') as f:
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
