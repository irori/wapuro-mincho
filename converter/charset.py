import codecs
import re


class JIS:
    def __init__(self, plane):
        if plane not in (1, 2):
            raise ValueError('Invalid JIS plane %d' % plane)
        self.plane = plane
        self.decoder = codecs.getdecoder('euc_jis_2004')
        self.encoder = codecs.getencoder('euc_jis_2004')

    def unicode(self, cp):
        # Convert JIS to EUC-JIS-2004 and then Unicode
        high = (cp >> 8) + 0x80
        low = (cp & 0xff) + 0x80
        if high > 0xff or low > 0xff:
            return None
        try:
            if self.plane == 2:
                euc = (0x8f, high, low)
            else:
                euc = (high, low)
            ustr, n = self.decoder(bytearray(euc))
            return ustr
        except UnicodeDecodeError:
            return None

    def decompose(self, ustr):
        names = []
        for u in ustr:
            try:
                euc, n = self.encoder(u)
                if euc[0] == 0x8f:
                    names.append(f'jis2-{euc[1] - 0xa0:02}-{euc[2] - 0xa0:02}')
                else:
                    names.append(f'jis1-{euc[0] - 0xa0:02}-{euc[1] - 0xa0:02}')
            except UnicodeEncodeError:
                names.append(f'u{ord(u):04X}')
        return ' '.join(names)


def codeconv(charset_registry, charset_encoding):
    if re.match(r'JISX\d+(\.\d+)?', charset_registry, flags=re.IGNORECASE):
        return JIS(int(charset_encoding))
    raise ValueError('Unsupported encoding "%s"' % charset_registry)


_variants_table = {}
def _add_variant(cps):
    for cp in cps:
        _variants_table[cp] = cps

_add_variant([0x3000, 0x20])  # IDEOGRAPHIC SPACE
for i in range(0xff01, 0xff5f):
    _add_variant([i - 0xfee0, i])  # Fullwidth ASCII variants
_add_variant([0xffe0, 0xa2])  # FULLWIDTH CENT SIGN
_add_variant([0xffe1, 0xa3])  # FULLWIDTH POUND SIGN
_add_variant([0xffe2, 0xac])  # FULLWIDTH NOT SIGN
# euc_jis_2004 maps 1-09-11 (MACRON) to U+00AF (MACRON) and 1-01-17 (OVERLINE) to U+FFE3 (FULLWIDTH MACRON).
_add_variant([0xffe3, 0x203e]) # FULLWIDTH MACRON <- OVERLINE
_add_variant([0xffe4, 0xa6])  # FULLWIDTH BROKEN BAR
_add_variant([0xffe5, 0xa5])  # FULLWIDTH YEN SIGN
_add_variant([0x2014, 0x2015])  # HORIZONTAL BAR / EM DASH

def variants(u):
    return _variants_table.get(u, [u])
