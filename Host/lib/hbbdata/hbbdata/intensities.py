"""
  Functions returning the various primary stress allowable intensities
"""

import scipy.interpolate as inter

import hbbdata.errors as errors
import hbbdata.plastic as plastic
from hbbdata.utility import load_code_table, bilinear_interpolate, load_code_1D, get_allowable_time

def S_m(material, temp, reduce_temp = None, time = None, RT = 20.0,
    no_reduction = False): #pylint: disable=C0103
  """
    Code time-independent allowable S_m as a function of temperature

    Parameters:
      material:     valid HBB Class A material
      temp:         temperature requested

    Optional:
      reduce_temp:  temperature to use for the strength reduction factor.
                    Default (None) means use the actual temperature
      time:         time or equivalent time, for applying strength reduction
                    factors
                    Default (None) does not apply a reduction
      RT:           the value of room temperature, for determining
                    the allowable
      no_reduction: override the time/temperature factors and return unaged
                    properties (Default False)

    Source:
      Code rules, strictly in Section II.  However a good summary
      is in HBB-2160 (3), (-b) to (-f)

      S_m is the minimum of:

        i)   1/3 * Su @ room temperature
        ii)  1/3 * Su @ temperature
        iii) 2/3 * Sy @ room tepmerature
        iv)  For 304, 316, A800H, and A617:
              90% * Sy @ temperature
             For the rest:
              2/3 * Sy @ temperature
  """
  errors.valid_mat(material)

  if reduce_temp is not None:
    use_temp = reduce_temp
  else:
    use_temp = temp

  if no_reduction:
    use_temp = None
    time = None

  values = [
      plastic.ultimate_tensile_stress(material, RT, reduce_temp = use_temp,
        time = time) / 3.0,
      plastic.ultimate_tensile_stress(material, temp, reduce_temp = use_temp,
        time = time)  / 3.0,
      2.0 * plastic.yield_stress(material, RT, reduce_temp = use_temp,
        time = time) / 3.0
      ]

  if material in ['316', '304', '800H', 'A617']:
    values.append(0.9 * plastic.yield_stress(material, temp,
      reduce_temp = use_temp, time = time))
  else:
    values.append(2.0 * plastic.yield_stress(material, temp,
      reduce_temp = use_temp, time = time) / 3.0)

  return min(values)

def S_t(material, temp, time, extrapolate = False): #pylint: disable=C0103
  """
    Code time-dependent allowable stress intensity S_t as a function
    of temperature and time

    Parameters:
      material:     valid HBB Class A material
      temp:         temperature, degree C
      time:         time, hours

    Optional:
      extrapolate:  extrapolate outside of Code tables
  """
  errors.valid_mat(material)

  data = load_code_table(material, 'St')

  if time < 1.0:
    time = 1.0

  try:
    return bilinear_interpolate(data, time, temp, logx = True, logy = False,
        logdata = True, extrapolate = extrapolate)
  except Exception:
    raise errors.OutofRange("temperature or time")

def time_S_t(material, temp, stress, extrapolate = True): #pylint: disable=C0103
  """
    Return Code value of time to a given S_t

    Parameters:
      material:     the HBB Class A material
      temp:         temperature
      stress:       S_t

    Optional:
      extrapolate:  extrapolate outside Code table
      ztol:         tolerance for checking if function value is flat
      bigmax:       big bracket value for brentq
  """
  errors.valid_mat(material)

  data = load_code_table(material, 'St')

  return get_allowable_time(data, temp, stress, extrapolate)

def S_mt(material, temp, time, extrapolate = False, reduce_temp = None, #pylint: disable=C0103
    effective_time = None, RT = 20.0, no_reduction = False):
  """
    Code S_mt allowable stress intensity as a function of temperature and time

    Parameters:
      material:     HBB Class A material
      temp:         temperature, in degrees C
      time:         time, hours

    Optional:
      extrapolate:      extrapolate off the Code table, applies only to
                        S_t
      reduce_temp:      temperature to use for time-temperature reduction factor,
                        defaults to actual temperature
      effective_time:   time for time-temperature reduction factor,
                        defaults to actual time
      RT:               room temperature for that part of the Sm definition
      no_reduction:     override the time/temperature factors and return unaged
                        properties
  """
  if effective_time is None:
    effective_time = time
  s_m = S_m(material, temp, reduce_temp = reduce_temp, time = time, RT = RT,
      no_reduction = no_reduction)
  s_t = S_t(material, temp, time, extrapolate = extrapolate)

  return min(s_m,s_t)


def S_o(material, temp): #pylint: disable=C0103
  """
    Code design allowable stress intensity S_o as a function of temperature

    Parameters:
      material:     HBB Class A material
      temp:         temperature, in degrees C
  """
  errors.valid_mat(material)

  data = load_code_1D(material, "So")
  ifn = inter.interp1d(data[:,0], data[:,1])

  return float(ifn(temp))
