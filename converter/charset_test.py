import unittest

from bdflib import reader
import charset


class JISTest(unittest.TestCase):

    def test_plane1(self):
        with open('bdf/jiskan24-2003-1.bdf', 'rb') as f:
            bdf = reader.read_bdf(f)
        cconv = charset.JIS(1)

        unmapped = 0
        single_cp = 0
        multi_cp = 0
        has_variants = 0
        unicode_to_jis = {}
        for jis in bdf.codepoints():
            unicode = cconv.unicode(jis)
            if unicode is None:
                unmapped += 1
            elif len(unicode) == 1:
                single_cp += 1
                variants = charset.variants(ord(unicode))
                # print([jis, unicode, variants])
                if len(variants) > 1:
                    has_variants += 1
                for v in variants:
                    if v in unicode_to_jis:
                        self.assertEqual(jis, unicode_to_jis[v], 'conflict mapping for U+%04X' % v)
                    unicode_to_jis[v] = jis
            else:
                multi_cp += 1

        self.assertEqual(unmapped, 39)
        self.assertEqual(single_cp, 8772)
        self.assertEqual(multi_cp, 25)
        self.assertEqual(has_variants, 102)

    def test_plane2(self):
        with open('bdf/jiskan24-2000-2.bdf', 'rb') as f:
            bdf = reader.read_bdf(f)
        cconv = charset.JIS(2)

        unmapped = 0
        unicode_to_jis = {}
        for jis in bdf.codepoints():
            unicode = cconv.unicode(jis)
            if unicode is None:
                unmapped += 1
            else:
                self.assertEqual(1, len(unicode))
                u = ord(unicode)
                variants = charset.variants(u)
                self.assertEqual(1, len(variants))
                if u in unicode_to_jis:
                    self.assertEqual(jis, unicode_to_jis[u], 'conflict mapping for U+%04X' % u)
                unicode_to_jis[u] = jis

        self.assertEqual(unmapped, 9)
        self.assertEqual(len(unicode_to_jis), 2436)

    def test_decompose(self):
        cconv = charset.JIS(1)
        self.assertEqual('jis1-04-11 u309A', cconv.decompose('\u304b\u309a'))
        self.assertEqual('jis1-11-64 jis1-11-68', cconv.decompose('\u02e5\u02e9'))