import unittest

import defcon

from font import Font


class FontTest(unittest.TestCase):

    def test_ufo_metrics(self):
        f = Font('bdf/jiskan24-2003-1.bdf')
        info = defcon.Info()
        f.set_ufo_metrics(info)
        self.assertEqual(info.unitsPerEm, 256)
        self.assertEqual(info.ascender, 228)
        self.assertEqual(info.descender, -28)
        self.assertEqual(info.capHeight, 220)
        self.assertEqual(info.xHeight, 140)


if __name__ == '__main__':
    unittest.main()
