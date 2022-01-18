import os
import pycodestyle
import unittest


class TestPEP8(unittest.TestCase):

    def test_submodules_pep8_style(self):
        """Test that lib and unittest modules conform to PEP8."""
        oStyle = pycodestyle.StyleGuide()
        result = oStyle.check_files(['./',
                                     '../sciarticle/',
                                     '../sciarticle/lib/'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_main_module_pep8_style(self):
        """Test that main module conform to PEP8."""
        for sFile in os.listdir('../'):
            sTestFile = sFile.endswith('.py')
            if sTestFile:
                oStyle = pycodestyle.StyleGuide()
                result = oStyle.check_files(['../' + sFile])
                self.assertEqual(result.total_errors, 0,
                                 "Found code style errors (and warnings).")


if __name__ == '__main__':
    unittest.main()
