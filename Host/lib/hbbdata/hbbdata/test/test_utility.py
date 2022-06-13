#pylint: disable=missing-docstring, invalid-name, unused-variable
import unittest
import numpy as np
import scipy.interpolate as inter
from hbbdata.utility import load_code_table, max_col_interpolate, bilinear_interpolate
from hbbdata.intensities import time_S_t, S_t

class TestInterpTime(unittest.TestCase):
  def test_interpolation(self):
    v1 = time_S_t("A617", 704, 27.0)

    times = np.array([30000.0,100000.0])
    vals = np.array([S_t("A617", 704, t) for t in times])

    ifn1 = lambda x: 10.0**(inter.interp1d(vals,np.log10(times),
      fill_value = "extrapolate")(x))
    v2 = ifn1(27.0)

    slope = np.diff(np.log10(times))/np.diff(vals)[0]
    ifn2 = lambda x: 10.0**(np.log10(times)[1]+slope*(x-vals[1]))
    v3 = ifn2(27.0)
    
    print(v1,v2)
    print("Implemented versus scipy")
    self.assertTrue(np.isclose(v1,v2,rtol=1e-2))
    print(v2,v3)
    print("Scipy versus manual")
    self.assertTrue(np.isclose(v2,v3,rtol=1e-2))

class TestInterpMaxCol(unittest.TestCase):
  def setUp(self):

    self.data_type = 'fatigue'

    self.max_col_data= {
    # data in the row_l, col_l, val
      '304': [
      [1e1, 470, 0.0465],
      [4e2, 415, 0.00965],
      [1e3, 585, 0.0047],
      [2e3, 700, 0.00276],
      [4e4, 645, 0.00162]
      ]
      }

    self.max_col_interp_data= {
    # data in the N0, e0, N1, e1, temp (note, two subsequent lines are required)
      '304': [
      [1e1, 0.051, 2e1, 0.036, 40],
      [1e1, 0.051, 2e1, 0.036, 40],
      ]
      }

    self.max_col_data_range= {
    # data in the row_l, col_l, val
      '304': [
      [1e8, 470, 0.0465],
      [1e3, 1e5, 0.0047],
      [1e8, 1e5, 0.00162]
      ]
      }

  def test_interp_max_col(self):
    '''
    check that intermediate temperatures are pushed to the right value
    '''
    for mat, testData in self.max_col_data.items():

      data = load_code_table(mat, self.data_type)

      for cycle, temp, expVal in testData:
        val = max_col_interpolate(data, temp, cycle)
        s = 'The utility max_col_interpolate does not return the proper value'
        self.assertTrue(np.isclose(val, expVal), s)

  def test_interp_max_col_out_of_range(self):
    '''
    check that max_col_interpolate raise an error for out of range values
    '''
    for mat, testData in self.max_col_data_range.items():
      data = load_code_table(mat, self.data_type)
      for cycle, temp, expVal in testData:
        with self.assertRaises(ValueError):
          val = max_col_interpolate(data, temp, cycle)

  def test_interp_max_col_value(self):
    '''
    check that linear and loglinear interpolation are done properly by implementing them manually
    '''
    for mat, testData in self.max_col_interp_data.items():

      data = load_code_table(mat, self.data_type)

      for N0, e0, N1, e1, temp in testData:
        # Linear
        Neval = 0.5*(N0 + N1)
        eeval = (Neval - N0)/(N1-N0)*(e1-e0) + e0
        val = max_col_interpolate(data, temp, Neval, log = False)
        s = 'Linear interpolation does not work properly \n'
        s = s + 'real {} comp {}'.format(eeval, val)
        self.assertTrue(np.isclose(val, eeval), s)

        # Log linear
        N0 = np.log10(N0)
        N1 = np.log10(N1)
        NevalLog = np.log10(Neval)
        eevalLog = (NevalLog - N0)/(N1-N0)*(e1-e0) + e0
        val = max_col_interpolate(data, temp, Neval, log = True)

        s = 'Log linear interpolation does not work properly \n'
        s = s + 'real {} comp {}'.format(eeval, val)
        self.assertTrue(np.isclose(val, eevalLog), s)


class testBilinearInterp(unittest.TestCase): # Common1dTest):
  def setUp(self):

    self.data_type = 'Sr'

    self.gridData = [
      [0, 1, 2],
      [0, 1],
      [[5, 7, 9],[11, 16, 21]]
      ]
    #the test assumes z = 3x*y+2x+6y+5'
    # y-x 0   1   2
    # 0   5   7   9
    # 1   11  16  21

    self.testValue = np.array([ [0.5, 0.5],[0.25,0.25], [1.25, 0.8] ])
    self.testValueOutOfRange = np.array([ [-1, 0.5], [0.5,-.25], [-.2,-.3],
                       [2.3, 0.5],[0.5,1.2],  [3,2] ])

  def test_bilinearInterp(self):
    '''
    the test assumes z = 3x*y+2x+6y+5'
    '''
    nData = np.shape(self.testValue )[0]
    for i in range (0, nData):
      x = self.testValue[i][0]
      y = self.testValue[i][1]
      valInt = bilinear_interpolate(self.gridData, x, y, logx = False,
          logy = False, extrapolate = False)

      realVal =  3*x*y + 2*x+ 6*y +5
      s = 'Bilinear interpolation does not work as expected'
      self.assertTrue(np.isclose(valInt,realVal), s)


  def test_bilinearInterpOutOfRange(self):
    '''
    check if the bilinear interpolation prevent extrapolation
    '''
    nData = np.shape(self.testValueOutOfRange )[0]
    for i in range (0, nData):
      x = self.testValueOutOfRange[i][0]
      y = self.testValueOutOfRange[i][1]

      with self.assertRaises(ValueError):
        val_int = bilinear_interpolate(self.gridData, x, y, logx = False,
            logy = False, extrapolate = False)
