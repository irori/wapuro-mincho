import unittest

from path import PathBuilder
from smoother import Smoother, BLACK, NW, NE, SE, SW

class SmootherTest(unittest.TestCase):

    def test_getitem(self):
        s = Smoother([[0, 1], [1, 0], [1, 1]])
        self.assertEqual(s.width, 2)
        self.assertEqual(s.height, 3)
        self.assertFalse(s[(0, 0)])
        self.assertTrue(s[(1, 2)])
        self.assertFalse(s[(1, -1)])
        self.assertFalse(s[(-1, 1)])
        self.assertFalse(s[(2, 1)])

    def test_smooth(self):
        s1 = Smoother([[0, 1], [1, 0]])
        s1.smooth()
        self.assertEqual(s1._bmp, [[0|SE, 1|NW|SE], [1|NW|SE, 0|NW]])

        s2 = Smoother([[1, 0, 0], [1, 0, 0], [1, 1, 1]])
        s2.smooth()
        self.assertEqual(s2._bmp, [[1, 0, 0], [1, 0, 0], [1, 1, 1]])

        s3 = Smoother([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]])
        s3.smooth()
        self.assertEqual(s3._bmp, [
            [0|SE, 1|NW, 1|NE, 0|SW],
            [1|NW, 0|NW, 0|NE, 1|NE],
            [1|SW, 0|SW, 0|SE, 1|SE],
            [0|NE, 1|SW, 1|SE, 0|NW]
        ])

    def test_draw_black(self):
        s = Smoother([[0]])
        pb = PathBuilder()
        s._draw_black(pb, 20, 30, BLACK)
        pb.optimize()
        self.assertEqual(pb.generate_paths(),
                         [[(20, 30), (30, 30), (30, 40), (20, 40)]])

    def test_draw_black2(self):
        s = Smoother([[0]])
        pb = PathBuilder()
        s._draw_black(pb, 0, 0, BLACK | NW | NE | SE | SW)
        pb.optimize()
        self.assertEqual(pb.generate_paths(),
                         [[(0, 3), (3, 0), (7, 0), (10, 3),
                           (10, 7), (7, 10), (3, 10), (0, 7)]])

    def test_draw_white(self):
        s = Smoother([[0]])
        pb = PathBuilder()
        s._draw_white(pb, 20, 30, NW)
        pb.optimize()
        self.assertEqual(pb.generate_paths(),
                         [[(20, 30), (27, 30), (20, 37)]])

    def test_draw_white2(self):
        s = Smoother([[0]])
        pb = PathBuilder()
        s._draw_white(pb, 0, 0, NW | NE | SE | SW)
        pb.optimize()
        self.assertEqual(pb.generate_paths(),
                         [[(0, 0), (10, 0), (10, 10), (0, 10)],
                          [(2, 5), (5, 8), (8, 5), (5, 2)]])

    def test_vectorize(self):
        s = Smoother([[0, 1], [1, 0]])
        s.smooth()
        self.assertEqual(s.vectorize(),
                         [[(0, 13), (13, 0), (20, 0), (20, 7), (7, 20), (0, 20)]])

    def test_vectorize_origin(self):
        s = Smoother([[0, 1], [1, 0]])
        s.smooth()
        self.assertEqual(s.vectorize(10, -10),
                         [[(10, 3), (23, -10), (30, -10), (30, -3), (17, 10), (10, 10)]])


if __name__ == '__main__':
    unittest.main()
