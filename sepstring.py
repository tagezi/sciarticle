
def sep_sring(sString):
    sString = sString.replace(" and ", ", ")
    sString = sString.replace("; ", ", ")
    sString = sString.replace(",,", ", ")
    sString = sString.replace("  ", " ")
    sString = sString.split(", ")


s = "a, and b, c, d, and g; v and o"
sep_sring(s)
