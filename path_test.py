import unittest

from path import PathBuilder, Pen


class PathBuilderTest(unittest.TestCase):

    def test_add(self):
        pb = PathBuilder()
        p1 = (10, 10)
        p2 = (20, 10)
        pb.add_segment(p1, p2)
        self.assertEqual(pb._segments, {p1: set([p2])})

    def test_cancel(self):
        pb = PathBuilder()
        p1 = (10, 10)
        p2 = (20, 10)
        pb.add_segment(p1, p2)
        pb.add_segment(p2, p1)
        self.assertEqual(pb._segments, {})

    def test_optimize(self):
        octagon = Pen(PathBuilder())
        octagon.move_to(2, 0)
        octagon.line_to(3, 0)
        octagon.line_to(4, 0)
        octagon.line_to(5, 1)
        octagon.line_to(6, 2)
        octagon.line_to(6, 3)
        octagon.line_to(6, 4)
        octagon.line_to(5, 5)
        octagon.line_to(4, 6)
        octagon.line_to(3, 6)
        octagon.line_to(2, 6)
        octagon.line_to(1, 5)
        octagon.line_to(0, 4)
        octagon.line_to(0, 3)
        octagon.line_to(0, 2)
        octagon.line_to(1, 1)
        octagon.line_to(2, 0)

        reference = Pen(PathBuilder())
        reference.move_to(2, 0)
        reference.line_to(4, 0)
        reference.line_to(6, 2)
        reference.line_to(6, 4)
        reference.line_to(4, 6)
        reference.line_to(2, 6)
        reference.line_to(0, 4)
        reference.line_to(0, 2)
        reference.line_to(2, 0)

        octagon.pb.optimize()
        self.assertEqual(octagon.pb._segments, reference.pb._segments)

    def test_optimize_seq(self):
        pen = Pen(PathBuilder())
        pen.move_to(0, 0)
        pen.line_to(0, 1)
        pen.line_to(0, 2)
        pen.line_to(0, 3)
        pen.line_to(3, 3)
        pen.line_to(0, 0)
        pen.pb.optimize()
        self.assertEqual(pen.pb._segments,
                         {(0,0): set([(0,3)]),
                          (0,3): set([(3,3)]),
                          (3,3): set([(0,0)])})

    def test_generate_paths(self):
        pen = Pen(PathBuilder())
        pen.move_to(0, 0)
        pen.line_to(3, 0)
        pen.line_to(3, 3)
        pen.line_to(0, 3)
        pen.line_to(0, 0)
        pen.move_to(1, 1)
        pen.line_to(1, 2)
        pen.line_to(2, 2)
        pen.line_to(2, 1)
        pen.line_to(1, 1)
        self.assertEqual(pen.pb.generate_paths(),
                         [[(0,0), (3,0), (3,3), (0,3)],
                          [(1,1), (1,2), (2,2), (2,1)]])


if __name__ == '__main__':
    unittest.main()
