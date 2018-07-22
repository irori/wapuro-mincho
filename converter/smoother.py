from path import PathBuilder, Pen

BLACK = 1
NW = 2 << 0
NE = 2 << 1
SE = 2 << 2
SW = 2 << 3

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
    #   |  |p2|p4|
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

    # For white cells, fills a corner. For black cells, clips a corner.
    def _clip(self, p, corner):
        self._bmp[p[1]][p[0]] |= 2 << corner

    def vectorize(self, ox=0, oy=0):
        pb = PathBuilder()
        for y in range(self.height):
            for x in range(self.width):
                n = self._bmp[y][x]
                if n & BLACK:
                    self._draw_black(pb, x + ox, y + oy, n)
                else:
                    self._draw_white(pb, x + ox, y + oy, n)
        pb.optimize()
        return pb.generate_paths()

    def _draw_black(self, pb, x, y, n):
        x = x * 10
        y = y * 10
        pen = Pen(pb)
        pen.move_to(x + 3, y)
        pen.line_to(x + 7, y)
        if not n & NE:
            pen.line_to(x + 10, y)
        pen.line_to(x + 10, y + 3)
        pen.line_to(x + 10, y + 7)
        if not n & SE:
            pen.line_to(x + 10, y + 10)
        pen.line_to(x + 7, y + 10)
        pen.line_to(x + 3, y + 10)
        if not n & SW:
            pen.line_to(x, y + 10)
        pen.line_to(x, y + 7)
        pen.line_to(x, y + 3)
        if not n & NW:
            pen.line_to(x, y)
        pen.line_to(x + 3, y)

    def _draw_white(self, pb, x, y, n):
        ox = x * 10
        oy = y * 10
        def draw(x1, y1, x2, y2):
            pb.add_segment((ox + x1, oy + y1), (ox + x2, oy + y2))

        if n & NW:
            draw(0,3, 0,0)
            draw(0,0, 3,0)
            if not n & NE:
                draw(7,0, 5,2)
            draw(5,2, 2,5)
            if not n & SW:
                draw(2,5, 0,7)
        if n & NE:
            draw(7,0, 10,0)
            draw(10,0, 10,3)
            if not n & SE:
                draw(10,7, 8,5)
            draw(8,5, 5,2)
            if not n & NW:
                draw(5,2, 3,0)
        if n & SE:
            draw(10,7, 10,10)
            draw(10,10, 7,10)
            if not n & SW:
                draw(3,10, 5,8)
            draw(5,8, 8,5)
            if not n & NE:
                draw(8,5, 10,3)
        if n & SW:
            draw(3,10, 0,10)
            draw(0,10, 0,7)
            if not n & NW:
                draw(0,3, 2,5)
            draw(2,5, 5,8)
            if not n & SE:
                draw(5,8, 7,10)
        if n & (NW | NE):
            draw(3,0, 7,0)
        if n & (NE | SE):
            draw(10,3, 10,7)
        if n & (SE | SW):
            draw(7,10, 3,10)
        if n & (SW | NW):
            draw(0,7, 0,3)


def shift(pos, delta):
    return (pos[0] + delta[0], pos[1] + delta[1])

def rshift(pos, delta):
    return (pos[0] - delta[0], pos[1] - delta[1])
