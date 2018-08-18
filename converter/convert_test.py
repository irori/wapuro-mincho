# -*- coding: utf-8 -*-
import unittest

from font import Font
import convert


class ConverterTest(unittest.TestCase):

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
            (0x411, 4, u'ワープロ明朝'),
        ]

        font = Font('bdf/jiskan24-2003-1.bdf')
        ufo = convert.create_ufo(font, limit=1)
        otf = convert.compile(ufo, 'out.ttf')
        actual = []
        for name in sorted(otf['name'].names):
            self.assertEqual(name.platformID, 3)
            self.assertEqual(name.platEncID, 1)
            actual.append((name.langID, name.nameID, name.toUnicode()))
        self.assertEqual(expected, actual)

    def test_h2x_name_table(self):
        expected = [
            # (langID, nameID, string)
            (0x409, 0, u'Public domain'),
            (0x409, 1, u'Wapuro Mincho YokoBaikaku'),
            (0x409, 2, u'Regular'),
            (0x409, 3, u'1.000;NONE;WapuroMincho-YokoBaikaku'),
            (0x409, 4, u'Wapuro Mincho YokoBaikaku'),
            (0x409, 5, u'Version 1.000'),
            (0x409, 6, u'WapuroMincho-YokoBaikaku'),
            (0x409, 11, u'https://irori.github.io/wapuro-mincho/'),
            (0x409, 16, u'Wapuro Mincho'),
            (0x409, 17, u'YokoBaikaku'),
            (0x411, 1, u'ワープロ明朝 横倍角'),
            (0x411, 4, u'ワープロ明朝 横倍角'),
            (0x411, 16, u'ワープロ明朝'),
            (0x411, 17, u'横倍角'),
        ]

        font = Font('bdf/jiskan24-2003-1.bdf')
        ufo = convert.create_ufo(font, limit=1)
        convert.h2x(ufo)
        otf = convert.compile(ufo, 'out.ttf')
        actual = []
        for name in sorted(otf['name'].names):
            self.assertEqual(name.platformID, 3)
            self.assertEqual(name.platEncID, 1)
            actual.append((name.langID, name.nameID, name.toUnicode()))
        self.assertEqual(expected, actual)

    def test_v2x_name_table(self):
        expected = [
            # (langID, nameID, string)
            (0x409, 0, u'Public domain'),
            (0x409, 1, u'Wapuro Mincho TateBaikaku'),
            (0x409, 2, u'Regular'),
            (0x409, 3, u'1.000;NONE;WapuroMincho-TateBaikaku'),
            (0x409, 4, u'Wapuro Mincho TateBaikaku'),
            (0x409, 5, u'Version 1.000'),
            (0x409, 6, u'WapuroMincho-TateBaikaku'),
            (0x409, 11, u'https://irori.github.io/wapuro-mincho/'),
            (0x409, 16, u'Wapuro Mincho'),
            (0x409, 17, u'TateBaikaku'),
            (0x411, 1, u'ワープロ明朝 縦倍角'),
            (0x411, 4, u'ワープロ明朝 縦倍角'),
            (0x411, 16, u'ワープロ明朝'),
            (0x411, 17, u'縦倍角'),
        ]

        font = Font('bdf/jiskan24-2003-1.bdf')
        ufo = convert.create_ufo(font, limit=1)
        convert.v2x(ufo)
        otf = convert.compile(ufo, 'out.ttf')
        actual = []
        for name in sorted(otf['name'].names):
            self.assertEqual(name.platformID, 3)
            self.assertEqual(name.platEncID, 1)
            actual.append((name.langID, name.nameID, name.toUnicode()))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
