# -*- coding: utf-8 -*-
import argparse
import sys

import defcon
from ufo2ft import compileOTF

from font import Font


def draw(glyph, ufo_glyph, smooth=True):
    for path in glyph.vectorize(smooth):
        contour = defcon.Contour()
        for p in path:
            contour.appendPoint(defcon.Point(p, 'line'))

        ufo_glyph.appendContour(contour)


def generate_otf(font, otf_filename, limit=None):
    ufo = defcon.Font()

    ufo.info.familyName = 'Wapuro Moji'
    ufo.info.styleName = 'Regular'
    ufo.info.styleMapFamilyName = 'Wapuro Moji'
    ufo.info.versionMajor = 0
    ufo.info.versionMinor = 1
    ufo.info.copyright = 'Public domain'
    ufo.info.openTypeOS2Type = []  # installable

    ufo.info.unitsPerEm = font.width
    ufo.info.descender = font.descent
    ufo.info.xHeight = font.ascent * 4 / 5
    ufo.info.capHeight = font.ascent
    ufo.info.ascender = font.ascent

    count = 0
    for g in font.glyphs():
        if len(g.unicode) > 1:
            print >> sys.stderr, 'Cannot convert unicode sequence %s' % g.unicode
            continue
        ufo_glyph = ufo.newGlyph(g.name())
        ufo_glyph.unicode = ord(g.unicode)
        ufo_glyph.width = font.width
        draw(g, ufo_glyph)

        count += 1
        if limit and count >= limit:
            break

    # ufo.save('out.ufo')
    ttf = compileOTF(ufo)

    ttf['name'].addMultilingualName({'ja': u'ワープロ文字'}, nameID=1)
    ttf['name'].addMultilingualName({'ja': u'ワープロ文字'}, nameID=4)

    ttf.save(otf_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', metavar='N', type=int, help='limit number of glyphs to convert')
    parser.add_argument('--out', metavar='FILENAME', help='output file name')
    parser.add_argument('bdf', help='input bdf file')
    args = parser.parse_args()

    font = Font(args.bdf)
    generate_otf(font, args.out, limit=args.limit)
