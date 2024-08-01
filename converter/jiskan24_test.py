import unittest

import defcon

from jiskan24 import Jiskan24


class Jiskan24Test(unittest.TestCase):

    def test_ufo_metrics(self):
        f = Jiskan24('bdf/jiskan24-2003-1.bdf')
        info = defcon.Info()
        f.set_ufo_metrics(info)
        self.assertEqual(info.unitsPerEm, 256)
        self.assertEqual(info.ascender, 228)
        self.assertEqual(info.descender, -28)
        self.assertEqual(info.capHeight, 200)
        self.assertEqual(info.xHeight, 140)

    def test_vectorize(self):
        f = Jiskan24('bdf/jiskan24-2003-1.bdf')

        em_dash = f.glyph(0x213d)
        paths = em_dash.vectorize()
        self.assertEqual(paths, [[(0, 90), (256, 90), (256, 100), (0, 100)]])

        v_em_dash = em_dash.vertical_variant()
        paths = v_em_dash.vectorize()
        self.assertEqual(paths, [[(118, -28), (128, -28), (128, 228), (118, 228)]])


if __name__ == '__main__':
    unittest.main()
