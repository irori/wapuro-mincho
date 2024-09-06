import unittest

import defcon

from jiskan24 import Jiskan24

JISX2013_CHARACTER_COUNT = 11233

class Jiskan24Test(unittest.TestCase):

    def test_ufo_metrics(self):
        f = Jiskan24(['bdf/jiskan24-2003-1.bdf'])
        info = defcon.Info()
        f.set_ufo_metrics(info)
        self.assertEqual(info.unitsPerEm, 1000)
        self.assertEqual(info.ascender, 880)
        self.assertEqual(info.descender, -120)
        self.assertEqual(info.capHeight, 760)
        self.assertEqual(info.xHeight, 532)

    def test_vectorize(self):
        f = Jiskan24(['bdf/jiskan24-2003-1.bdf'])

        em_dash = f.glyph(0x213d)
        paths = em_dash.vectorize()
        self.assertEqual(paths, [[(0, 342), (1000, 342), (1000, 380), (0, 380)]])

        v_em_dash = em_dash.vertical_variant()
        paths = v_em_dash.vectorize()
        self.assertEqual(paths, [[(462, -120), (500, -120), (500, 880), (462, 880)]])

    def test_glyphs(self):
        f = Jiskan24(['bdf/jiskan24-2003-1.bdf', 'bdf/jiskan24-2000-2.bdf'])
        glyphs = list(f.glyphs())
        self.assertEqual(len(glyphs), JISX2013_CHARACTER_COUNT)


if __name__ == '__main__':
    unittest.main()
