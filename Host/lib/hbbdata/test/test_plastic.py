#pylint: disable=missing-docstring
import unittest
from test.common import CommonCodeTableTests
import numpy as np
import hbbdata.plastic

class TestTensileReduction(unittest.TestCase, CommonCodeTableTests):
  def setUp(self):
    self.forward = hbbdata.plastic.tensile_strength_reduction_factor
    self.backward = None
    self.true_data = {
        '304': [
          [625,   1,       0.80],
          [525,   30,      0.80],
          [625,   100,     0.80],
          [550,   10000,   0.80],
          [475,   10000,   1.00],
          [525,   30000,   0.80],
          [575,   30000,   0.80],
          [450,   100000,  1.00],
          [575,   300000,  0.80]
          ],

        '316': [
          [625,   1,       0.80],
          [525,   30,      0.80],
          [625,   100,     0.80],
          [550,   10000,   0.80],
          [475,   10000,   1.00],
          [525,   30000,   0.80],
          [575,   30000,   0.80],
          [450,   100000,  1.00],
          [575,   300000,  0.80]
          ],

        '2.25Cr-1Mo': [
          [625,   1,       1.00],
          [525,   30,      1.00],
          [625,   100,     0.94],
          [550,   10000,   0.84],
          [475,   10000,   0.98],
          [525,   30000,   0.84],
          [575,   30000,   0.75],
          [450,   100000,  0.93],
          [575,   300000,  0.65]
          ],
        'gr91': [
          [   375,  3000,     1.00],
          [   625,  1,        1.00],
          [   525,  30,       1.00],
          [   625,  100,      1.00],
          [   550,  10000,    1.00],
          [   475,  10000,    1.00],
          [   525,  30000,    1.00],
          [   575,  30000,    0.92],
          [   450,  100000,   1.00],
          [   575,  300000,   0.83],
          ],
        '800H': [
          [625,   1,       1.00],
          [525,   30,      1.00],
          [625,   100,     1.00],
          [550,   10000,   1.00],
          [475,   10000,   1.00],
          [525,   30000,   1.00],
          [750,   30000,   0.90],
          [450,   100000,  1.00],
          [575,   300000,  1.00]
          ],
        'A617': [
          [625,   1,       1.00],
          [525,   30,      1.00],
          [625,   100,     1.00],
          [550,   10000,   1.00],
          [475,   10000,   1.00],
          [525,   30000,   1.00],
          [575,   30000,   1.00],
          [450,   100000,  1.00],
          [575,   300000,  1.00]
          ]
          }


class TestReducedTensile(unittest.TestCase):
  def setUp(self):
    self.forward = hbbdata.plastic.ultimate_tensile_stress
    self.true_data = {
        '304': [
          [650,   1,  251.2]],
        '316': [
          [650,   1,  277.6]],
        '2.25Cr-1Mo': [
          [650,   1,  202]],
        'gr91': [
          [650,   1,  228]],
        '800H': [
          [650,   1,  345]],
        'A617': [
          [650,   1,  540.0]],
          }

  def test_ultimate_tensile_stress(self):

    for mat, test_data in self.true_data.items():
      for temp, time, real_val in test_data:
        comp_val = self.forward(mat, temp, time = time)
        msg = "\n Test yield stress Failed \n"
        msg += "Mat: {} Temp: {} real_value: {} computed_value: {} \n".format(
            mat, temp, real_val, comp_val)
        self.assertTrue(np.isclose(comp_val, real_val),msg)


class TestYieldReduction(unittest.TestCase, CommonCodeTableTests):
  def setUp(self):
    self.forward = hbbdata.plastic.yield_strength_reduction_factor
    self.backward = None
    self.true_data = {
        '304': [
          [625,   1,       1.00],
          [525,   30,      1.00],
          [625,   100,     1.00],
          [550,   10000,   1.00],
          [475,   10000,   1.00],
          [525,   30000,   1.00],
          [575,   30000,   1.00],
          [450,   100000,  1.00],
          [575,   300000,  1.00]
          ],

        '316': [
          [625,   1,       1.00],
          [525,   30,      1.00],
          [625,   100,     1.00],
          [550,   10000,   1.00],
          [475,   10000,   1.00],
          [525,   30000,   1.00],
          [575,   30000,   1.00],
          [450,   100000,  1.00],
          [575,   300000,  1.00]
          ],

        '2.25Cr-1Mo': [
          [625,   1,       1.00],
          [525,   30,      1.00],
          [625,   100,     0.99],
          [550,   1000,    0.98],
          [600,   10000,   0.00],
          [525,   30000,   0.88],
          [500,   100000,  0.89],
          [575,   300000,  0.66]
          ],
        'gr91': [
          [   375,  3000,     1.00],
          [   625,  1,        1.00],
          [   525,  30,       1.00],
          [   625,  100,      1.00],
          [   550,  10000,    1.00],
          [   475,  10000,    1.00],
          [   525,  30000,    1.00],
          [   575,  30000,    1.00],
          [   450,  100000,   1.00],
          [   575,  300000,   1.00],
          ],
        '800H': [
          [625,   1,       1.00],
          [525,   30,      1.00],
          [625,   100,     1.00],
          [550,   10000,   1.00],
          [475,   10000,   1.00],
          [525,   30000,   1.00],
          [750,   30000,   0.90],
          [450,   100000,  1.00],
          [575,   300000,  1.00]
          ],
        'A617': [
          [625,   1,       1.00],
          [525,   30,      1.00],
          [625,   100,     1.00],
          [550,   10000,   1.00],
          [475,   10000,   1.00],
          [525,   30000,   1.00],
          [575,   30000,   1.00],
          [450,   100000,  1.00],
          [575,   300000,  1.00]
          ]
          }

class TestReducedYield(unittest.TestCase):
  def setUp(self):
    self.forward = hbbdata.plastic.yield_stress
    self.true_data = {
        '304': [
          [650,   1,  97]],
        '316': [
          [650,   1,  110]],
        '2.25Cr-1Mo': [
          [650,   300,  97.9]], #0.89
        'gr91': [
          [650,   1,  165]],
        '800H': [
          [800,   1,  78.21]],
        'A617': [
          [650,   1,  161.0]],
          }

  def test_yield_stress(self):

    for mat, test_data in self.true_data.items():
      for temp, time, real_val in test_data:
        comp_val = self.forward(mat, temp, time = time)
        msg = "\n Test yield stress \n"
        msg += "Mat: {} Temp: {} real_value: {} computed_value: {} \n".format(
            mat, temp, real_val, comp_val)
        self.assertTrue(np.isclose(comp_val, real_val),msg)
