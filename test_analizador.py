import unittest
import math
from analizador_matematico import AnalizadorMatematico

class AnalizadorTests(unittest.TestCase):
    def setUp(self):
        self.a = AnalizadorMatematico()

    def test_paraboloides(self):
        r = self.a.calcular_numerico(lambda x,y: 8-x*x-y*y, lambda x,y: x*x+y*y,
            (-2,2), (lambda x: -math.sqrt(max(0,4-x*x)), lambda x: math.sqrt(max(0,4-x*x))))
        self.assertAlmostEqual(r['volumen'],16*math.pi,places=6)

    def test_invalid_surfaces(self):
        for f in (lambda x,y: float('nan'), lambda x,y: -1):
            with self.assertRaises(ValueError):
                self.a.calcular_numerico(f,lambda x,y: 0,(0,1),(lambda x: 0,lambda x: 1))

    def test_evaluation_error(self):
        with self.assertRaises(ZeroDivisionError):
            self.a.calcular_numerico(lambda x,y: 1/0,lambda x,y: 0,(0,1),(lambda x: 0,lambda x: 1))

if __name__ == '__main__':
    unittest.main()
