import codecs
import re


class JIS:
    def __init__(self):
        self.decoder = codecs.getdecoder('euc_jis_2004')

    def unicode(self, cp):
        # Convert JIS to EUC-JIS-2004 and then Unicode
        high = (cp >> 8) + 0x80
        low = (cp & 0xff) + 0x80
        if high > 0xff or low > 0xff:
            return None
        try:
            ustr, n = self.decoder(bytearray((high, low)))
            return ustr
        except UnicodeDecodeError:
            return None


def codeconv(charset_registry, charset_encoding):
    if re.match(r'JISX\d+(\.\d+)?', charset_registry, flags=re.IGNORECASE):
        return JIS()
    raise RuntimeError('Unsupported encoding "%s"' % charset_registry)
