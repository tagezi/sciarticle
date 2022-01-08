import sys
import unittest

sys.path.append('../')
from strmain import *
from perfectSoup import *


class TestStrMainFunctions(unittest.TestCase):

    def test_strmain_get_value(self):
        sString = 'a b, c,d;i; f and g,and j'
        self.assertEqual(get_values(sString), ['a b', 'c', 'd', 'i', 'f', 'g', 'j'])
        with self.assertRaises(TypeError):
            sString.split(1)

    def test_strmain_add_zero(self):
        self.assertEqual(add_zero('2021'), '2021')
        self.assertEqual(add_zero('22'), '22')
        self.assertEqual(add_zero('3'), '03')

    def test_strmain_clean_spaces(self):
        self.assertEqual(clean_spaces('a b'), 'a b')
        self.assertEqual(clean_spaces(' a b '), 'a b')
        self.assertEqual(clean_spaces('a\xa0b '), 'a b')
        self.assertEqual(clean_spaces(' a b\xa0'), 'a b')

    def test_srtmain_clean_parens(self):
        self.assertEqual(clean_parens('a(b)'), 'a')
        self.assertEqual(clean_parens('a(b d)'), 'a')
        self.assertEqual(clean_parens('a b (d 12)'), 'a b')

    def test_strmain_iri_to_uri(self):
        sQueryString = 'https://en.wikipedia.org/wiki/Americän_Journal_of_Law_&_Medicine'
        sAnsverSrting = 'https://en.wikipedia.org/wiki/Americ%C3%A4n_Journal_of_Law_%26_Medicine'
        self.assertEqual(iri_to_uri(sQueryString), sAnsverSrting)

    def test_strmain_get_filename_time(self):
        sQueryString = 'backup.file/main.file.csv'
        tTime = time.localtime()
        sTime = str(tTime.tm_year) + add_zero(str(tTime.tm_mon)) + add_zero(str(tTime.tm_mday)) + \
                add_zero(str(tTime.tm_hour)) + add_zero(str(tTime.tm_min)) + add_zero(str(tTime.tm_sec))
        lDirAndFile = splitext(sQueryString)
        sAnsverSrting = lDirAndFile[0] + "_" + sTime + lDirAndFile[-1]
        self.assertEqual(get_filename_time(sQueryString), sAnsverSrting)


if __name__ == '__main__':
    unittest.main()
