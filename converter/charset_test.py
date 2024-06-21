import unittest

from bdflib import reader
import charset


class JISTest(unittest.TestCase):

    def test_jis(self):
        with open('bdf/jiskan24-2003-1.bdf', 'rb') as f:
            bdf = reader.read_bdf(f)
        cconv = charset.JIS(1)

        single_cp = 0
        multi_cp = 0
        has_variants = 0
        unicode_to_cp = {}
        for cp in bdf.codepoints():
            unicode = cconv.unicode(cp)
            if unicode is None:
                pass
            elif len(unicode) == 1:
                single_cp += 1
                variants = charset.variants(ord(unicode))
                # print([cp, unicode, variants])
                if len(variants) > 1:
                    has_variants += 1
                for v in variants:
                    if v in unicode_to_cp:
                        self.assertEqual(cp, unicode_to_cp[v], 'conflict mapping for U+%04X' % v)
                    unicode_to_cp[v] = cp
            else:
                multi_cp += 1

        self.assertEqual(single_cp, 8772)
        self.assertEqual(multi_cp, 25)
        self.assertEqual(has_variants, 101)
