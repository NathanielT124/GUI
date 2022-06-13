#pylint: disable=too-many-return-statements, too-many-branches
"""
  This module returns Code values of yield stress and ultimate tensile stress
"""

import scipy.interpolate as inter

import hbbdata.errors as errors
from hbbdata.utility import load_code_1D, load_code_table, bilinear_interpolate

def yield_stress(material, temp, reduce_temp = None, time = None):
  """
    Code Sy as a function of temperature

    Parameters:
      material:      the HBB class A material
      temperature:   the temperature(s) to return values for, C

    Optional:
      reduce_temp:   temperature to use for the strength reduction factor
                     Default (None) means use the actual temperature
      time:          service time or equivalent service time @ temperature,
                     for applying strength reduction factor
                     Default (None) implies no reduction
  """

  data = load_code_1D(material,"yield")
  ifn = inter.interp1d(data[:,0], data[:,1])

  if reduce_temp is not None:
    use_temp = reduce_temp
  else:
    use_temp = temp

  if time is not None:
    factor = yield_strength_reduction_factor(material, time, use_temp)
  else:
    factor = 1.0

  try:
    return factor * ifn(temp)
  except ValueError:
    raise errors.OutofRange("temperature")

def ultimate_tensile_stress(material, temp, reduce_temp = None,
    time = None):
  """
    Code Su as a function of temperature

    Parameters:
      material:      the HBB class A material
      temperature:   the temperature(s) to return values for, C

    Optional:
      reduce_temp:   temperature to use for the strength reduction factor
                     Default (None) means use the actual temperature
      time:          service time or equivalent service time @ temperature,
                     for applying strength reduction factor
                     Default (None) implies no reduction
  """
  data = load_code_1D(material,"ultimate")
  ifn = inter.interp1d(data[:,0], data[:,1])

  if reduce_temp is not None:
    use_temp = reduce_temp
  else:
    use_temp = temp

  if time is not None:
    factor = tensile_strength_reduction_factor(material, time, use_temp)
  else:
    factor = 1.0

  try:
    return factor * ifn(temp)
  except ValueError:
    raise errors.OutofRange("temperature")

def yield_strength_reduction_factor(material, time, temp):
  """
    Return the yield strength reduction factor for the given
    material, time, and temperature.

    Parameters:
      material:      the HBB class A material
      time:          time (in hours) of service @ temperature
      temperature:   service temperature, degrees C
  """
  errors.valid_mat(material)

  if material == '304':
    if temp >= 480.0:
      return 1.0
    else:
      return 1.0
  elif material == '316':
    if temp >= 480.0:
      return 1.0
    else:
      return 1.0
  elif material == '800H':
    if temp >= 730.0:
      return 0.9
    else:
      return 1.0
  elif material == 'A617':
    if temp >= 425.0:
      return 1.0
    else:
      return 1.0
  elif material == '2.25Cr-1Mo':
    if temp >= 425.0:
      if time < 1.0:
        return 1.0
      data = load_code_table(material, 'reduction_yield')
      return bilinear_interpolate(data, time, temp)
    else:
      return 1.0
  elif material == 'gr91':
    if temp >= 480.0:
      return 1.0
    else:
      return 1.0
  else:
    raise errors.UnknownMaterial(material)

def tensile_strength_reduction_factor(material, time, temp): #pylint: disable=invalid-name
  """
    Return the tensile strength reduction factor for the given
    material, time, and temperature.

    Parameters:
      material:      the HBB class A material
      time:          time (in hours) of service @ temperature
      temperature:   service temperature, degrees C
  """
  errors.valid_mat(material)

  if material == '304':
    if temp >= 480.0:
      return 0.80
    else:
      return 1.0
  elif material == '316':
    if temp >= 480.0:
      return 0.80
    else:
      return 1.0
  elif material == '800H':
    if temp >= 730.0:
      return 0.9
    else:
      return 1.0
  elif material == 'A617':
    if temp >= 425.0:
      return 1.0
    else:
      return 1.0
  elif material == '2.25Cr-1Mo':
    if temp >= 425.0:
      if time < 1.0:
        return 1.0
      data = load_code_table(material, 'reduction_tensile')
      return bilinear_interpolate(data, time, temp)
    else:
      return 1.0
  elif material == 'gr91':
    if temp >= 480.0:
      if time < 1.0:
        return 1.0
      data = load_code_table(material, 'reduction_tensile')
      return bilinear_interpolate(data, time, temp)
    else:
      return 1.0
  else:
    raise errors.UnknownMaterial(material)
