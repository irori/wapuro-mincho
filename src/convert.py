# -*- coding: utf-8 -*-
import argparse
import os
import sys

import defcon
from ufo2ft import compileTTF, compileOTF

import jisx0213
from jiskan24 import Jiskan24


def draw(glyph, ufo_glyph, smooth=True):
    for path in glyph.vectorize(smooth):
        contour = defcon.Contour()
        for p in path:
            contour.appendPoint(defcon.Point(p, 'line'))

        ufo_glyph.appendContour(contour)


def japanese_name_record(nameID, string):
    return {
        'platformID': 3,
        'encodingID': 1,
        'languageID': 0x411,
        'nameID': nameID,
        'string': string
    }


def create_ufo(jiskan, limit=None):
    ufo = defcon.Font()

    ufo.info.familyName = 'Wapuro Mincho'
    ufo.info.styleName = 'Regular'
    ufo.info.styleMapFamilyName = 'Wapuro Mincho'
    ufo.info.versionMajor = 1
    ufo.info.versionMinor = 2
    ufo.info.copyright = 'Public domain'
    ufo.info.openTypeNameManufacturerURL = 'https://irori.github.io/wapuro-mincho/'
    ufo.info.openTypeNameRecords = [
        japanese_name_record(1, u'ワープロ明朝'),
        japanese_name_record(4, u'ワープロ明朝'),
    ]
    ufo.info.openTypeOS2Type = []  # installable

    jiskan.set_ufo_metrics(ufo.info)

    vert_feature = []
    liga_feature = []

    count = 0
    for g in jiskan.glyphs():
        ufo_glyph = ufo.newGlyph(g.name())

        if len(g.unicode) == 1:
            ufo_glyph.unicodes = jisx0213.variants(ord(g.unicode))
        else:
            glyph_seq = jiskan.codeconv.decompose(g.unicode)
            liga_feature.append(' sub %s by %s;' % (glyph_seq, g.name()))

        ufo_glyph.width = jiskan.width
        ufo_glyph.height = jiskan.ascent - jiskan.descent
        draw(g, ufo_glyph)

        vg = g.vertical_variant()
        if vg is not None:
            ufo_vglyph = ufo.newGlyph(vg.name())
            ufo_vglyph.width = jiskan.width
            ufo_vglyph.height = jiskan.ascent - jiskan.descent
            draw(vg, ufo_vglyph)
            vert_feature.append(' sub %s by %s;' % (g.name(), vg.name()))

        if g.unicode == '\u309c':  # KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK
            # Add COMBINING KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK which is used in ligatures.
            u309a = ufo.insertGlyph(ufo_glyph, 'u309A')
            u309a.unicode = 0x309a

        count += 1
        if limit and count >= limit:
            break

    features = ''
    if len(vert_feature) > 0:
        features += 'feature vert {\n' + '\n'.join(vert_feature) + '\n} vert;\n'
    if len(liga_feature) > 0:
        features += 'feature liga {\n' + '\n'.join(liga_feature) + '\n} liga;\n'
    ufo.features.text = features

    print('%d glyphs converted' % count)
    return ufo


def h2x(ufo):
    ufo.info.styleMapFamilyName = 'Wapuro Mincho YokoBaikaku'
    ufo.info.styleName = 'YokoBaikaku'
    ufo.info.openTypeNameRecords = [
        japanese_name_record(1, u'ワープロ明朝 横倍角'),
        japanese_name_record(4, u'ワープロ明朝 横倍角'),
        japanese_name_record(16, u'ワープロ明朝'),
    ]
    ufo.info.openTypeNameRecords.append(japanese_name_record(17, u'横倍角'))
    ufo.info.openTypeVheaVertTypoAscender *= 2
    ufo.info.openTypeVheaVertTypoDescender *= 2
    for glyph in ufo:
        glyph.width *= 2
        for contour in glyph:
            for point in contour:
                point.x *= 2


def v2x(ufo):
    ufo.info.styleMapFamilyName = 'Wapuro Mincho TateBaikaku'
    ufo.info.styleName = 'TateBaikaku'
    ufo.info.openTypeNameRecords = [
        japanese_name_record(1, u'ワープロ明朝 縦倍角'),
        japanese_name_record(4, u'ワープロ明朝 縦倍角'),
        japanese_name_record(16, u'ワープロ明朝'),
    ]
    ufo.info.openTypeNameRecords.append(japanese_name_record(17, u'縦倍角'))

    ufo.info.ascender *= 2
    ufo.info.descender *= 2
    ufo.info.capHeight *= 2
    ufo.info.xHeight *= 2

    for glyph in ufo:
        glyph.height *= 2
        for contour in glyph:
            for point in contour:
                point.y *= 2


def compile(ufo, out_filename):
    ext = os.path.splitext(out_filename)[1]

    if ext == '.ttf':
        out = compileTTF(ufo)
    elif ext == '.otf':
        out = compileOTF(ufo)
    elif ext == '.woff':
        out = compileOTF(ufo, optimizeCFF=False)
        out.flavor = 'woff'
    elif ext == '.woff2':
        out = compileOTF(ufo, optimizeCFF=False)
        out.flavor = 'woff2'
    else:
        raise RuntimeError('Unknown output file type: %s' % ext)

    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', metavar='N', type=int, help='limit number of glyphs to convert')
    parser.add_argument('--out', metavar='FILENAME', help='output file name')
    parser.add_argument('--style', metavar='h2x|v2x', help='style')
    parser.add_argument('bdf', help='input bdf file', nargs='+')
    args = parser.parse_args()

    if len(args.bdf) == 1 and os.path.splitext(args.bdf[0])[1] == '.ufo':
        ufo = defcon.Font(args.bdf[0])
    else:
        jiskan = Jiskan24(args.bdf)
        ufo = create_ufo(jiskan, limit=args.limit)

    if args.style == 'h2x':
        h2x(ufo)
    elif args.style == 'v2x':
        v2x(ufo)

    if os.path.splitext(args.out)[1] == '.ufo':
        ufo.save(args.out, structure='zip')
    else:
        out = compile(ufo, args.out)
        out.save(args.out)
