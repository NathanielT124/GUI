"""
  Module returns rupture stresses and times from Section III, Division 5
"""

from hbbdata.utility import bilinear_interpolate, load_code_table, get_allowable_time
import hbbdata.errors as errors

def S_r(material, temp, time, extrapolate = False): # pylint: disable=C0103
  """
    Returns the Code Sr value

    Parameters:
      material:      the HBB Class A material
      temp:          the temperature to get data for, C
      time:          the time to get data for, hrs

    Optional:
      extrapolate:   extrapolate out of the table
  """
  errors.valid_mat(material)

  data = load_code_table(material, 'Sr')

  return bilinear_interpolate(data, time, temp, logx = True, logy = False,
      logdata = True, extrapolate = extrapolate)

def time_rupture(material, temp, stress, extrapolate = True):
  """
    Returns the Code value of time to rupture

    Parameters:
      material:      the HBB Class A material
      temp:          the temperature to get data for, C
      stress:        the rupture stress, MPa

    Optional:
      extrapolate:   if true, extrapolate out of the table
      ztol:          tolerance for checking if the function value is flat
      bigmax:        maximum time for extrapolation
  """
  errors.valid_mat(material)

  data = load_code_table(material, 'Sr')

  return get_allowable_time(data, temp, stress, extrapolate)
