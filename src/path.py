class PathBuilder:
    def __init__(self):
        self._segments = dict()

    def add_segment(self, p1, p2):
        s2 = self._segments.get(p2)
        if s2 and p1 in s2:
            s2.remove(p1)
            if not s2:
                del self._segments[p2]
        else:
            self._segments.setdefault(p1, set()).add(p2)

    def optimize(self):
        for p1 in list(self._segments.keys()):
            if p1 not in self._segments:
                continue
            for p2 in list(self._segments[p1]):
                while p2:
                    s2 = self._segments[p2]
                    p3 = next((p3 for p3 in s2 if collinear(p1, p2, p3)), None)

                    if p3:
                        self._segments[p1].add(p3)
                        self._segments[p1].remove(p2)
                        s2.remove(p3)
                        if not s2:
                            del self._segments[p2]
                        p2 = p3
                    else:
                        p2 = None

    def generate_paths(self):
        paths = []
        while self._segments:
            p = sorted(self._segments.keys())[0]
            path = []
            while p in self._segments:
                path.append(p)
                s = self._segments[p]
                p2 = s.pop()
                if not s:
                    del self._segments[p]
                p = p2
            paths.append(path)
        return paths


class Pen:
    def __init__(self, pb):
        self.pb = pb
        self.current = None

    def move_to(self, x, y):
        self.current = (x, y)

    def line_to(self, x, y):
        self.pb.add_segment(self.current, (x, y))
        self.current = (x, y)

def collinear(p1, p2, p3):
    (x1, y1) = p1
    (x2, y2) = p2
    (x3, y3) = p3
    return (y1 - y2) * (x1 - x3) == (y1 - y3) * (x1 - x2)
