import unittest

from bdflib import reader
import charset


class JISTest(unittest.TestCase):

    def test_jis(self):
        with open('bdf/jiskan24-2003-1.bdf', 'rb') as f:
            bdf = reader.read_bdf(f)
        cconv = charset.JIS()

        single_cp = 0
        multi_cp = 0
        for cp in bdf.codepoints():
            unicode = cconv.unicode(cp)
            if unicode is None:
                pass
            elif len(unicode) == 1:
                single_cp += 1
            else:
                multi_cp += 1

        self.assertEqual(single_cp, 8772)
        self.assertEqual(multi_cp, 25)
