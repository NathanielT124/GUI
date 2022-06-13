"""
  This module implements various temperature limits used in the Code
"""

import scipy.optimize as opt

import hbbdata.errors as errors
import hbbdata.intensities as intensities

def T_max(material):
  """
    The hot temperature as defined by HAA-1330-1

    Parameters:
      material:      the HBB class A material
  """
  errors.valid_mat(material)

  database = {'304': 425, '316': 425, '800H': 425, 'A617': 425,
      'gr91': 370, '2.25Cr-1Mo': 370, 'A740H': 425}

  try:
    return database[material]
  except Exception:
    raise errors.MissingData(material)

def Sr_max_T(material):
  """
    The hot temperature as defined by HAA-1330-1

    Parameters:
      material:      the HBB class A material
  """
  errors.valid_mat(material)

  database = {'304': 800, '316': 800, '800H': 900, 'A617': 950,
      'gr91': 650, '2.25Cr-1Mo': 650, 'A740H': 950}

  try:
    return database[material]
  except Exception:
    raise errors.MissingData(material)

def Sm_St(material, time = 100000.0, ll = 425.0, ul = 600.0):
  """
    The S_m == S_t for 100,000 hours criteria used in HBB-T

    Parameters:
      material:      the HBB class A material

    Optional:
      time:          the time to use in the equality, default 100,000 hours
      ll:            lower limit to use in solving for the critical point
      ul:            upper limit to use in solving for the critical point
  """
  if material == "A740H":
    ul = 800.0

  fn = lambda T: intensities.S_m(material, T) - intensities.S_t(material, T,
      time, extrapolate = True)

  return opt.brentq(fn, ll, ul)
