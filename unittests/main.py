import unittest
import unit_test_strmain
import unit_test_perfectsoup


def suite():
    calcTestSuite = unittest.TestSuite()
    calcTestSuite.addTest(unittest.makeSuite(unit_test_strmain.TestStrMainFunctions))
    calcTestSuite.addTest(unittest.makeSuite(unit_test_perfectsoup.TestPerfectSoupFunctions))

    return calcTestSuite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
