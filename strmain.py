import re
from urllib.parse import urlparse, quote, urlunparse


def get_values(sString):
    sString = sString.replace(" and ", ", ")
    sString = sString.replace("; ", ", ")
    sString = sString.replace(",,", ", ")
    sString = sString.replace("  ", " ")
    lString = sString.split(", ")

    return lString


def clean_parens(sString):
    if type(sString) == int:
        sString = str(sString)

    return re.sub(r'\([^()]*\)', '', sString).strip()


def iriToUri(iri):
    iri = re.sub(r'\n|\s+$', '', iri)

    if len(iri) != len(iri.encode()):
        parts = urlparse(iri)
        partUri = quote(parts[2], safe='/')
        listParamUri = (parts[0], parts[1], partUri, parts[3], parts[4], parts[5])
        try:
            uri = urlunparse(listParamUri)
        except ValueError as e:
            print("не пахает, потому что " + str(e))
            return None

        return uri

    return iri
