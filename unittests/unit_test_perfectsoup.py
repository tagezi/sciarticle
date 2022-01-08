import sys
import unittest

sys.path.append('../')
from perfectSoup import *


class TestPerfectSoupFunctions(unittest.TestCase):

    def test_perfectsoup_get_html(self):
        sQueryString = 'https://en.wikipedia.org/wiki/American_Journal_of_Law_&_Medicine'
        html = urlopen('https://ru.wikipedia.org/')
        self.assertEqual(type(get_html(sQueryString)), type(BeautifulSoup(html, "html5lib")))