#pylint: disable=missing-docstring,no-member,invalid-name, unused-variable
import numpy as np

from hbbdata import errors

class Common1dTest(object):
  def test_values(self):
    """
     Test all the interpolates against the references
    """
    for mat, data in self.true_data.items():
      for T, real_val in data:
        s =     "\n ---------------------------------------------\n"
        s = s + "Interpolated value not equal to the true one\n"
        comp_value = self.getter(mat, T)

        s = s + "Mat: {} Temp: {} real_value: {} computed_value: {}".format(
            mat, T, real_val, comp_value)

        self.assertTrue(np.isclose(real_val, comp_value), s)

  def test_bounds(self):
    """
     Test upper and lower bound errors
    """
    for mat, Ts in self.too_high.items():
      for T in Ts:
        with self.assertRaises(errors.OutofRange):
          print(mat, T)
          val = self.getter(mat, T)


    for mat, Ts in self.too_low.items():
      for T in Ts:
        with self.assertRaises(errors.OutofRange):
          val = self.getter(mat, T)

  def test_invalid(self):
    """
     Test to make sure we can't get data for materials that don't exist
    """
    T_invalid = 300.0
    invalid_mats = ['invalid_1', '300_invalid']

    for mat in invalid_mats:
      with self.assertRaises(errors.UnknownMaterial):
        val = self.getter(mat, T_invalid)

class CommonCodeTableTests(object):
  def test_table_value(self):
    """
    this test check that table values are correct and that proper value
    can be retrieved given the number of cycle and temperature
    """
    for mat, truedata in self.true_data.items():
      for x, temp, val in truedata:
        code_value = self.forward(mat, temp, x)
        self.assertTrue(np.isclose(code_value, val), "Forward check for material %s "
            "does not agree for (%f,%f) -> %f" % (mat, temp, x, val))

  def test_reverse_values(self):
    """
      This test checks the inverse function call for 2D tables
    """
    if self.backward is None:
      return

    for mat, truedata in self.true_data.items():
      for x, temp, val in truedata:
        code_value = self.backward(mat, temp, val)
        self.assertTrue(np.isclose(code_value, x, rtol = 1e-2), "Backward check for material %s "
            "does not agree for (%f,%f) -> %f != %f" % (mat, temp, val, x, code_value))
