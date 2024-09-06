import sys

from bdflib import reader

from jisx0213 import JISX0213
from smoother import Smoother, SCALE
from vertical import vertical_glyph

MARGIN = 44

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
        return Glyph(self.font, vg, self.unicode)

    def vectorize(self, smooth=True):
        s = Smoother(self._bitmap())
        if smooth:
            s.smooth()
        ox = MARGIN
        oy = -self.font.bdf[b'FONT_DESCENT'] * SCALE
        paths = s.vectorize(ox, oy)
        if self.should_occupy_imaginary_body():
            for path in paths:
                for i in range(len(path)):
                    x, y = path[i]
                    if x == ox:
                        x = 0
                    elif x == ox + self.bdf_glyph.bbW * SCALE:
                        x += MARGIN
                    if y == oy:
                        y -= MARGIN
                    elif y == oy + self.bdf_glyph.bbH * SCALE:
                        y += MARGIN
                    path[i] = (x, y)
        return paths

    def _bitmap(self):
        bitmap = []
        width = self.bdf_glyph.bbW
        for line in self.bdf_glyph.data:
            a = []
            for b in range(width - 1, -1, -1):
                a.append(line & (1 << b) and 1 or 0)
            bitmap.append(a)
        return bitmap

    def should_occupy_imaginary_body(self):
        if len(self.unicode) != 1:
            return False
        u = ord(self.unicode)
        if u == 0x2014 or u == 0x2015:  # HORIZONTAL BAR / EM DASH
            return True
        if 0x2500 <= u <= 0x257f:  # BOX DRAWINGS
            return True
        return False


class Jiskan24:
    def __init__(self, bdf_filenames):
        with open(bdf_filenames[0], 'rb') as f:
            self.bdf = reader.read_bdf(f)
            if self.bdf[b'CHARSET_ENCODING'] != b'1':
                raise ValueError('Primary BDF is not JIS X 0213 plane 1')
        for filename in bdf_filenames[1:]:
            with open(filename, 'rb') as f:
                bdf = reader.read_bdf(f)
                plane = int(bdf[b'CHARSET_ENCODING'])
                cp_offset = (plane - 1) * 0x8080
                for g in bdf.glyphs:
                    self.bdf.new_glyph_from_data(
                        g.name,
                        g.data,
                        g.bbX,
                        g.bbY,
                        g.bbW,
                        g.bbH,
                        g.advance,
                        g.codepoint + cp_offset)

        self.codeconv = JISX0213()
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
            g = self.glyph(cp)
            if g is not None:
                yield g

    def glyph(self, cp):
        unicode = self.codeconv.unicode(cp)
        if unicode is None:
            return None
        return Glyph(self, self.bdf[cp], unicode)
