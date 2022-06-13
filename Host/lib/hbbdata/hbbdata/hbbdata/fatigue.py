"""
  Functions returning Code fatigue curve data and generated related data.
"""

import scipy.optimize as opt

import hbbdata.errors as errors
from hbbdata.utility import load_code_table, max_col_interpolate

def strain_to_failure(material, maxtemp, cycles, extrapolate = True):
  """
    Strain to failure for a given number of cycles

    Parameters:
      material:      HBB Class A material
      maxtemp:       maximum cycle temperature
      cycles:        number of cycles

    Optional:
      extrapolate:   extrapolate outside the table (Default=True)
  """

  data = load_code_table(material,'fatigue')

  try:
    return max_col_interpolate(data, maxtemp, cycles, log = True,
        extrapolate = extrapolate)
  except errors.ColumnOutofRange as ex:
    raise ex
  except Exception:
    raise errors.OutofRange("cycles")

def cycles_to_failure(material, maxtemp, erange, extrapolate = True,
    cycles_min = 0.0, cycles_max = 1.0e12):
  """
    Number of cycles to failure for a given strain range

    Parameters:
      material:      HBB Class A material
      maxtemp:       maximum cycle temperature
      erange:        strain range

    Optional:
      extrapolate:   extrapolate outside the table (Default=True)
      cycles_min:    minimum number of cycles, for Brent's method (Default=0.0)
      cycles_max:    maximum number of cycles, for Brent's method (Default=1.0e12)
  """

  data = load_code_table(material,'fatigue')

  ifn = lambda N: max_col_interpolate(data, maxtemp, N, log = True,
      extrapolate = extrapolate, use_close = True)

  try:
    return opt.brentq(lambda N: erange - ifn(N), cycles_min, cycles_max)
  except Exception:
    raise errors.OutofRange("temperature or strain range")
