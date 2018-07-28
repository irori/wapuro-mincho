import sys

from bdflib import reader

from charset import codeconv
from smoother import Smoother


class Glyph:
    def __init__(self, font, bdf_glyph, unicode):
        self.font = font
        self.bdf_glyph = bdf_glyph
        self.unicode = unicode

    def name(self):
        return self.bdf_glyph.name

    def vectorize(self, smooth=True):
        s = Smoother(self._bitmap())
        if smooth:
            s.smooth()
        return s.vectorize(1, -self.font.bdf['FONT_DESCENT'])

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
        with open(bdf_filename) as f:
            self.bdf = reader.read_bdf(f)
        self.codeconv = codeconv(self.bdf['CHARSET_REGISTRY'],
                                 self.bdf['CHARSET_ENCODING'])
        self.width = (self.bdf[self.bdf['DEFAULT_CHAR']].bbW + 2) * 10
        self.ascent = (self.bdf['FONT_ASCENT'] + 1) * 10
        self.descent = (self.bdf['FONT_DESCENT'] + 1) * -10
        self.xheight = (self._xheight() + 1) * 10

        # For some reasons, IDEOGRAPHIC SPACE in jiskan24-2003-1.bdf is not
        # really a whitespace. Overwrite it.
        self.bdf[0x2121].data = map(lambda _: 0, self.bdf[0x2121].data)

    def glyphs(self):
        for cp in self.bdf.codepoints():
            unicode = self.codeconv.unicode(cp)
            if unicode is None:
                print >> sys.stderr, 'Unknown codepoint 0x%x:' % cp
                print >> sys.stderr, self.bdf[cp]
                continue
            yield Glyph(self, self.bdf[cp], unicode)

    def _xheight(self):
        return self.bdf[0x2378].get_ascent()  # FULLWIDTH LATIN SMALL LETTER X
