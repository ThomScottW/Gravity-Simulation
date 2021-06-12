import unittest
import math

from SimModel import Vector


class VectorTests(unittest.TestCase):
    def test_vector_magnitude(self):
        """Perform basic tests of the Vector class's magnitude method."""
        vec1 = Vector(5, 4)  # Vector with x = 5 and y = 4

        self.assertEqual(vec1.magnitude(), math.sqrt(41))
    
    def test_float_vector_magnitude(self):
        """Test the vector's magnitude method with floating point x and y components."""
        x = 4.523
        y = 9.2421

        vec1 = Vector(x, y)

        self.assertEqual(vec1.magnitude(), math.hypot(x, y))

    def test_unit_vector(self):
        """Make sure the unit vector is properly computed."""
        vec1 = Vector(5, 4)
        expected = Vector(5 / math.sqrt(41), 4 / math.sqrt(41))

        vec1_unit = vec1.unit()

        self.assertEqual(vec1_unit.magnitude(), expected.magnitude())

    def test_dot_product(self):
        vec1 = Vector(7, 1123.2)
        vec2 = Vector(5, 22)

        result = vec1.dot_product(vec2)
        expected = 24745.4

        self.assertEqual(result, expected)

    def test_addition(self):
        vec1 = Vector(9, 10)
        vec2 = Vector(66, 21)

        result = (vec1 + vec2).magnitude()
        expected = Vector(75, 31).magnitude()

        self.assertEqual(result, expected)

    def test_multiplication(self):
        vec1 = Vector(3, 4)
        factor = 22.4
        
        # Perform the multiplication
        result_vector = vec1 * factor
        result_magnitude = result_vector.magnitude()

        expected_magnitude = 112

        # Had to use almost equal because it was off by a tiny amount, althought still
        # basically correct
        self.assertAlmostEqual(result_magnitude, expected_magnitude)

        




        





if __name__ == '__main__':
    unittest.main()