#!/usr/bin/env python
import sys
from bdflib import model, reader, writer

_ROT90 = 1
_ROT90FLIP = 2

_CONVERSION_TABLE = {
    0x2122: (None, (15, 16)),
    0x2123: (None, (15, 15)),
    0x2131: (_ROT90, None),
    0x2132: (_ROT90, None),
    0x213c: (_ROT90FLIP, None),
    0x213d: (_ROT90, None),
    0x213e: (_ROT90, None),
    0x2141: (_ROT90FLIP, None),
    0x2142: (_ROT90, None),
    0x2143: (_ROT90, (0, -1)),
    0x2144: (_ROT90, None), # FIXME
    0x2145: (_ROT90, None), # FIXME
    0x214a: (_ROT90, None),
    0x214b: (_ROT90, None),
    0x214c: (_ROT90, None),
    0x214d: (_ROT90, None),
    0x214e: (_ROT90, None),
    0x214f: (_ROT90, None),
    0x2150: (_ROT90, None),
    0x2151: (_ROT90, None),
    0x2152: (_ROT90FLIP, None),
    0x2153: (_ROT90FLIP, None),
    0x2154: (_ROT90, None),
    0x2155: (_ROT90, None),
    0x2156: (_ROT90, None),
    0x2157: (_ROT90, None),
    0x2158: (_ROT90, None),
    0x2159: (_ROT90, None),
    0x215a: (_ROT90, None),
    0x215b: (_ROT90, None),
    0x2161: (_ROT90, None),
    0x2421: (None, (3, 3)),
    0x2423: (None, (3, 4)),
    0x2425: (None, (3, 3)), # FIXME
    0x2427: (None, (2, 3)),
    0x2429: (None, (3, 3)),
    0x2443: (None, (3, 3)),
    0x2463: (None, (4, 3)),
    0x2465: (None, (3, 3)),
    0x2467: (None, (2, 3)),
    0x246e: (None, (3, 3)),
    0x2521: (None, (4, 3)),
    0x2523: (None, (3, 3)),
    0x2525: (None, (4, 3)),
    0x2527: (None, (4, 4)),
    0x2529: (None, (4, 3)),
    0x2543: (None, (4, 3)),
    0x2563: (None, (3, 3)),
    0x2565: (None, (3, 4)),
    0x2567: (None, (4, 4)),
    0x256e: (None, (3, 3)),
    0x2575: (None, (3, 3)),
    0x2576: (None, (4, 3)),
}

def vertical_glyph(glyph):
    if glyph.codepoint not in _CONVERSION_TABLE:
        return None
    rot, dxdy = _CONVERSION_TABLE[glyph.codepoint]
    vg = model.Glyph(glyph.name + 'v', None,
                     glyph.bbX, glyph.bbY, glyph.bbW, glyph.bbH,
                     glyph.advance, glyph.codepoint)
    data = glyph.data
    if rot is _ROT90:
        data = _rotate90(data, glyph.bbW)
    elif rot is _ROT90FLIP:
        data = _rotate90(reversed(data), glyph.bbW)
    if dxdy is not None:
        data = _translate(data, dxdy)
    if glyph.codepoint == 0x213c:
        data[1] <<= 1
    vg.data = data
    return vg


def _rotate90(data, w):
    out = [0] * w
    for row in data:
        for col in range(w):
            out[col] = (out[col] << 1) + (row & (1 << col) and 1 or 0)
    return out


def _translate(data, dxdy):
    dx, dy = dxdy
    if dx > 0:
        data = [row >> dx for row in data]
    if dx < 0:
        data = [row << -dx for row in data]
    if dy > 0:
        dy -= len(data)
    if dy < 0:
        data = data[-dy:] + data[:-dy]
    return data


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        bdf = reader.read_bdf(f)

    out = model.Font('vertical', bdf['POINT_SIZE'],
                     bdf['RESOLUTION_X'], bdf['RESOLUTION_Y'])

    for cp in bdf.codepoints():
        vg = vertical_glyph(bdf[cp])
        if vg is None:
            continue
        out.glyphs.append(vg)
        out.glyphs_by_codepoint[cp] = vg

    writer.write_bdf(out, sys.stdout)
