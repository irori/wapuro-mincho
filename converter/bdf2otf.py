# -*- coding: utf-8 -*-
import argparse
import os
import sys

import defcon
from ufo2ft import compileTTF, compileOTF

from font import Font


def draw(glyph, ufo_glyph, smooth=True):
    for path in glyph.vectorize(smooth):
        contour = defcon.Contour()
        for p in path:
            contour.appendPoint(defcon.Point(p, 'line'))

        ufo_glyph.appendContour(contour)


def generate_otf(font, out_filename, limit=None):
    ufo = defcon.Font()

    ufo.info.familyName = 'Wapuro Mincho'
    ufo.info.styleName = 'Regular'
    ufo.info.styleMapFamilyName = 'Wapuro Mincho'
    ufo.info.versionMajor = 0
    ufo.info.versionMinor = 1
    ufo.info.copyright = 'Public domain'
    ufo.info.openTypeOS2Type = []  # installable

    font.set_ufo_metrics(ufo.info)

    count = 0
    for g in font.glyphs():
        if len(g.unicode) > 1:
            print >> sys.stderr, 'Cannot convert unicode sequence %s' % g.unicode
            continue
        ufo_glyph = ufo.newGlyph(g.name())

        # Associate halfwidth characters too
        u = ord(g.unicode)
        if u == 0x3000:
            ufo_glyph.unicodes = [u, 0x20]
        elif 0xff01 <= u <= 0xff5e:
            ufo_glyph.unicodes = [u, u - 0xfee0]
        else:
            ufo_glyph.unicode = u

        ufo_glyph.width = font.width
        draw(g, ufo_glyph)

        count += 1
        if limit and count >= limit:
            break

    print('%d glyphs converted' % count)

    ext = os.path.splitext(out_filename)[1]
    if ext == '.ufo':
        ufo.save(out_filename)
        return

    otf = None
    if ext == '.ttf':
        otf = compileTTF(ufo)
    elif ext == '.otf':
        otf = compileOTF(ufo)
    elif ext == '.woff2':
        otf = compileOTF(ufo, optimizeCFF=False)
        otf.flavor = 'woff2'
    else:
        raise RuntimeError('Unknown output file type: %s' % ext)

    otf['name'].addMultilingualName({'ja': u'ワープロ明朝'}, nameID=1)
    otf['name'].addMultilingualName({'ja': u'ワープロ明朝'}, nameID=4)
    otf.save(out_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', metavar='N', type=int, help='limit number of glyphs to convert')
    parser.add_argument('--out', metavar='FILENAME', help='output file name')
    parser.add_argument('bdf', help='input bdf file')
    args = parser.parse_args()

    font = Font(args.bdf)
    generate_otf(font, args.out, limit=args.limit)
