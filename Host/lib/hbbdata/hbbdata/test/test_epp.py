#pylint: disable=missing-docstring
import unittest
import hbbdata.epp as epp
import numpy as np

class TestEPP_pseudoyield_N862(unittest.TestCase):
  def setUp(self):
    self.forward = epp.pseudoyield_N862

    self.true_data = {
    # data t_prime, temp
        '304': [
          [200, 1 ,   144.],
          [800, 1 ,   69],
          [800, 10 ,  65*0.9],
          ],
        'gr91': [
          [450, 10 ,   337],
          [450, 30 ,   337],
          [450, 100,   337],
          [450, 300,   337],
          [450, 1000,  337],
          [450, 3000,  337],
          [450, 10000, 337],
          [450, 30000, 329],
          [450, 100000,308],
          [450, 300000,289],
          [575, 10 ,   231],
          [575, 30 ,   213],
          [575, 100,   194],
          [575, 300,   179],
          [575, 1000,  163],
          [575, 3000,  149],
          [575, 10000, 135],
          [575, 30000, 122],
          [575, 100000,110],
          [575, 300000,99]
          ]
        }

  def test_pseudoyield_N862(self):
    for mat, test_data in self.true_data.items():
      for temp, time, real_val in test_data:
        comp_val = self.forward(mat, time, [temp])
        msg = "\n Test pseudoyield_N862 Failed \n"
        msg += "Mat: {} Temp: {}, Time {} real_value: {} computed_value: {} \n".format(
            mat, temp, time, real_val, comp_val)
        self.assertTrue(np.isclose(comp_val, real_val),msg)
