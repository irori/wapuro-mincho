import argparse
import codecs
import sys

from jiskan24 import Jiskan24


def svg_path(glyph, smooth=True):
    s = []
    for path in glyph.vectorize(smooth):
        for i, p in enumerate(path):
            if i == 0:
                s.append('M')
            elif i == 1:
                s.append('L')
            s.append('%d,%d' % p)
        s.append('z')
    return ' '.join(s)


def generate_svg(font, limit=None):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    print '<?xml version="1.0"?>'
    print '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >'
    print '<svg xmlns="http://www.w3.org/2000/svg">'
    print '<defs>'
    print '<font id="wordpro" horiz-adv-x="%d">' % font.width
    print '<font-face font-family="wordpro" units-per-em="%d" ascent="%d" descent="%d"/>' % (font.width, font.ascent, font.descent)

    count = 0
    for g in font.glyphs():
        print '<glyph unicode="%s" d="%s"/>' % (g.unicode, svg_path(g))
        count += 1
        if limit and count >= limit:
            break

    print '</font></defs></svg>'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', metavar='N', type=int, help='limit number of glyphs to convert')
    parser.add_argument('bdf', help='input bdf file')
    args = parser.parse_args()

    font = Jiskan24(args.bdf)
    generate_svg(font, limit=args.limit)
