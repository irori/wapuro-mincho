import sys

from bdflib import reader

from charset import codeconv
from smoother import Smoother, SCALE
from vertical import vertical_glyph

MARGIN = 8

class Glyph:

    def __init__(self, font, bdf_glyph, unicode):
        self.font = font
        self.bdf_glyph = bdf_glyph
        self.unicode = unicode

    def name(self):
        return 'jis' + self.bdf_glyph.name.decode('ascii')

    def vertical_variant(self):
        vg = vertical_glyph(self.bdf_glyph)
        if vg is None:
            return None
        return Glyph(self.font, vg, None)

    def vectorize(self, smooth=True):
        s = Smoother(self._bitmap())
        if smooth:
            s.smooth()
        return s.vectorize(MARGIN, -self.font.bdf[b'FONT_DESCENT'] * SCALE)

    def _bitmap(self):
        bitmap = []
        width = self.bdf_glyph.bbW
        for line in self.bdf_glyph.data:
            a = []
            for b in range(width - 1, -1, -1):
                a.append(line & (1 << b) and 1 or 0)
            bitmap.append(a)
        return bitmap


class Font:
    def __init__(self, bdf_filename):
        with open(bdf_filename, 'rb') as f:
            self.bdf = reader.read_bdf(f)
        self.codeconv = codeconv(self.bdf[b'CHARSET_REGISTRY'].decode('ascii'),
                                 self.bdf[b'CHARSET_ENCODING'].decode('ascii'))
        self.width = self.bdf[self.bdf[b'DEFAULT_CHAR']].bbW * SCALE + MARGIN * 2
        self.ascent = self.bdf[b'FONT_ASCENT'] * SCALE + MARGIN
        self.descent = -self.bdf[b'FONT_DESCENT'] * SCALE - MARGIN

        # For some reasons, IDEOGRAPHIC SPACE in jiskan24-2003-1.bdf is not
        # really a whitespace. Overwrite it.
        self.bdf[0x2121].data = map(lambda _: 0, self.bdf[0x2121].data)

    def set_ufo_metrics(self, info):
        info.unitsPerEm = self.width
        info.openTypeOS2TypoLineGap = 0
        info.ascender = self.ascent
        info.descender = self.descent
        info.capHeight = self.bdf[0x2354].get_ascent() * SCALE  # FULLWIDTH LATIN CAPITAL LETTER T
        info.xHeight = self.bdf[0x2378].get_ascent() * SCALE  # FULLWIDTH LATIN SMALL LETTER X
        info.postscriptIsFixedPitch = True
        info.openTypeVheaVertTypoAscender = info.unitsPerEm // 2
        info.openTypeVheaVertTypoDescender = info.unitsPerEm // 2
        info.openTypeVheaVertTypoLineGap = 0

    def glyphs(self):
        for cp in self.bdf.codepoints():
            unicode = self.codeconv.unicode(cp)
            if unicode is None:
                print('Unknown codepoint 0x%x:' % cp, file=sys.stderr)
                print(self.bdf[cp], file=sys.stderr)
                continue
            yield Glyph(self, self.bdf[cp], unicode)
