# -*- coding: utf-8 -*-
import unittest

from font import Font
import bdf2otf


class Bdf2OtfTest(unittest.TestCase):

    def test_name_table(self):
        expected = [
            # (langID, nameID, string)
            (0x409, 0, u'Public domain'),
            (0x409, 1, u'Wapuro Mincho'),
            (0x409, 2, u'Regular'),
            (0x409, 3, u'1.000;NONE;WapuroMincho-Regular'),
            (0x409, 4, u'Wapuro Mincho Regular'),
            (0x409, 5, u'Version 1.000'),
            (0x409, 6, u'WapuroMincho-Regular'),
            (0x409, 11, u'https://irori.github.io/wapuro-mincho/'),
            (0x411, 1, u'ワープロ明朝'),
            (0x411, 4, u'ワープロ明朝')
        ]

        font = Font('bdf/jiskan24-2003-1.bdf')
        ufo = bdf2otf.create_ufo(font, limit=1)
        otf = bdf2otf.compile(ufo, 'out.ttf')
        actual = []
        for name in sorted(otf['name'].names):
            self.assertEqual(name.platformID, 3)
            self.assertEqual(name.platEncID, 1)
            actual.append((name.langID, name.nameID, name.toUnicode()))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
