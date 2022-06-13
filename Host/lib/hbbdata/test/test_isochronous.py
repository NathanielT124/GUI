#pylint: disable=missing-docstring
import unittest
import hbbdata.isochronous as issc
import hbbdata.elastic as elastic
import numpy as np

class TestRealxationAnalysis(unittest.TestCase):
  def setUp(self):
    # data for relaxation analysis: time, stress, Temperture
    self.test_data_points = {'A617':[[100, 400, 500], [100, 300, 800]]}

  # testing is performed only for A617 because there is a clsoed form solution
  def test_realxation_analysis(self):
    mat = 'A617'
    for time, stress, T in self.test_data_points[mat]:
      E = elastic.youngs(mat, T)
      nu = elastic.poissons(mat)

      Ta = T + 273.15
      A = -4.480
      B1 = -3.174
      B2 = -2.510
      T0 = 775.0
      eps0 = 1.656e7
      kboltz = 1.38064e-23 * 1000.0
      b = 2.019 * 1.0e-7

      if T <= T0:
        B = B2
      else:
        B = B1

      mu = E/(2*(1+nu))

      a = -E*eps0 * np.exp(mu*B*b**3.0/(A * kboltz * Ta))
      c = (-mu * b**3.0 / (A * kboltz * Ta))
      b = mu
      q = stress

      # from mathematica
      real_stress = b**(c/(-1 + c))*(-1 + c)**(1/( 1 - c))* \
        ((b**c*q**(1 - c))/(-1 + c) - a*time)**(1/(1 - c))

      comp_stress = issc.relaxation_analysis_rate(mat, T, stress, [time,2*time], dt = 0.01)


      msg = "\n Test RealxationAnalysis stress \n"
      msg += "Mat: {} T: {} real_value: {} computed_value: {}\n".format(
          mat, T, real_stress, comp_stress[1])
      self.assertTrue(np.isclose(comp_stress[1], real_stress),msg)

  def test_realxation_analysis_no_creep(self):
    mat = 'A617'
    T = 500
    time = 10
    real_stress = 5

    comp_stress = issc.relaxation_analysis_rate(mat, T, 5, [time,2*time], dt = 0.01)


    msg = "\n Test RealxationAnalysis stress no Creep\n"
    msg += "Mat: {} T: {} real_value: {} computed_value: {}\n".format(
        mat, T, real_stress, comp_stress[1])
    self.assertTrue(np.isclose(comp_stress[1], real_stress),msg)
