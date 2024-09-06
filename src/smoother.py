from path import PathBuilder, Pen

SCALE = 38

BLACK = 1
NW = 2 << 0
NE = 2 << 1
SE = 2 << 2
SW = 2 << 3

C3 = 12
C5 = SCALE // 2
C2 = C5 - C3
C7 = SCALE - C3
C8 = SCALE - C2
C10 = SCALE

class Smoother:

    def __init__(self, bitmap):
        self.height = len(bitmap)
        self.width = len(bitmap[0])
        self._bmp = bitmap

    # self[(x, y)] returns true if (x, y) is inside the bounding box and black.
    def __getitem__(self, p):
        x, y = p
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self._bmp[y][x] & 1 and True or False

    def smooth(self):
        for y in range(self.height):
            for x in range(self.width):
                self._interpolate((x, y))

    # Interpolates the bitmap at p0.
    #   +--+--+--+
    #   |p7|p2|p4|
    #   +--+--+--+
    #   |p1|p0|p6|
    #   +--+--+--+
    #   |p3|p5|  |
    #   +--+--+--+
    #
    # - If (!p0 & p1 & p2 & !(p3 & p4)):
    #   - The top-left corner of p0 is filled.
    #   - If !(p3 | p5), the bottom-right corner of p1 is clipped.
    #   - If !(p4 | p6), the bottom-right corner of p2 is clipped.
    #   - If !p7, the bottom-right corner of p7 is filled.
    # Repeat the above for all four directions.
    def _interpolate(self, p0):
        if self[p0]:
            return
        dirs = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, 0))
        for dir in range(4):
            p1 = shift(p0, dirs[dir])
            p2 = shift(p0, dirs[dir + 1])
            p3 = rshift(p1, dirs[dir + 1])
            p4 = rshift(p2, dirs[dir])
            if not (self[p1] and self[p2] and not (self[p3] and self[p4])):
                continue
            self._clip(p0, dir)
            p5 = rshift(p0, dirs[dir + 1])
            p6 = rshift(p0, dirs[dir])
            if not self[p3] and not self[p5]:
                self._clip(p1, (dir + 2) % 4)
            if not self[p4] and not self[p6]:
                self._clip(p2, (dir + 2) % 4)
            p7 = shift(p2, dirs[dir])
            if not self[p7]:
                self._clip(p7, (dir + 2) % 4)

    # For white cells, fills a corner. For black cells, clips a corner.
    def _clip(self, p, corner):
        self._bmp[p[1]][p[0]] |= 2 << corner

    def vectorize(self, ox=0, oy=0):
        pb = PathBuilder()
        for y in range(self.height):
            for x in range(self.width):
                n = self._bmp[y][x]
                if n & BLACK:
                    self._draw_black(pb, x*SCALE + ox, y*SCALE + oy, n)
                else:
                    self._draw_white(pb, x*SCALE + ox, y*SCALE + oy, n)
        pb.optimize()
        return pb.generate_paths()

    def _draw_black(self, pb, x, y, n):
        pen = Pen(pb)
        pen.move_to(x + C3, y)
        pen.line_to(x + C7, y)
        if not n & NE:
            pen.line_to(x + C10, y)
        pen.line_to(x + C10, y + C3)
        pen.line_to(x + C10, y + C7)
        if not n & SE:
            pen.line_to(x + C10, y + C10)
        pen.line_to(x + C7, y + C10)
        pen.line_to(x + C3, y + C10)
        if not n & SW:
            pen.line_to(x, y + C10)
        pen.line_to(x, y + C7)
        pen.line_to(x, y + C3)
        if not n & NW:
            pen.line_to(x, y)
        pen.line_to(x + C3, y)

    def _draw_white(self, pb, x, y, n):
        def draw(x1, y1, x2, y2):
            pb.add_segment((x + x1, y + y1), (x + x2, y + y2))

        if n & NW:
            draw(0,C3, 0,0)
            draw(0,0, C3,0)
            if not n & NE:
                draw(C7,0, C5,C2)
            draw(C5,C2, C2,C5)
            if not n & SW:
                draw(C2,C5, 0,C7)
        if n & NE:
            draw(C7,0, C10,0)
            draw(C10,0, C10,C3)
            if not n & SE:
                draw(C10,C7, C8,C5)
            draw(C8,C5, C5,C2)
            if not n & NW:
                draw(C5,C2, C3,0)
        if n & SE:
            draw(C10,C7, C10,C10)
            draw(C10,C10, C7,C10)
            if not n & SW:
                draw(C3,C10, C5,C8)
            draw(C5,C8, C8,C5)
            if not n & NE:
                draw(C8,C5, C10,C3)
        if n & SW:
            draw(C3,C10, 0,C10)
            draw(0,C10, 0,C7)
            if not n & NW:
                draw(0,C3, C2,C5)
            draw(C2,C5, C5,C8)
            if not n & SE:
                draw(C5,C8, C7,C10)
        if n & (NW | NE):
            draw(C3,0, C7,0)
        if n & (NE | SE):
            draw(C10,C3, C10,C7)
        if n & (SE | SW):
            draw(C7,C10, C3,C10)
        if n & (SW | NW):
            draw(0,C7, 0,C3)


def shift(pos, delta):
    return (pos[0] + delta[0], pos[1] + delta[1])

def rshift(pos, delta):
    return (pos[0] - delta[0], pos[1] - delta[1])
