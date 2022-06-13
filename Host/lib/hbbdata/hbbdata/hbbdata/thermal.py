"""
  This module return thermal properties (coefficient of thermal expansion,
  thermal conductivity, and thermal diffusivity) from Section II
"""

import scipy.interpolate as inter

import hbbdata.errors as errors
from hbbdata.utility import load_code_1D

def cte(material, temp, extrapolate = False):
  """
    The code specified instantaneous CTE as a function of temperature

    Parameters:
      material:      the HBB class A material
      temp:          the temperature(s) to return values for, C

    Optional:
      extrapolate:   if true extrapolate properties
  """

  data=load_code_1D(material,"cte")

  if extrapolate:
    ifn = inter.interp1d(data[:,0], data[:,1]*1.0e-6, fill_value = "extrapolate")
  else:
    ifn = inter.interp1d(data[:,0], data[:,1]*1.0e-6)

  try:
    return ifn(temp)
  except ValueError:
    raise errors.OutofRange("temperature")


def ctc(material, temp, extrapolate = False):
  """
    The code specified instantaneous CTC as a function of temperature

    Parameters:
      material:      the HBB class A material
      temp:          the temperature(s) to return values for, C

    Optional:
      extrapolate:   if true extrapolate properties
  """

  data=load_code_1D(material,"ctc")

  if extrapolate:
    ifn = inter.interp1d(data[:,0], data[:,1], fill_value = "extrapolate")
  else:
    ifn = inter.interp1d(data[:,0], data[:,1])

  try:
    return ifn(temp)
  except ValueError:
    raise errors.OutofRange("temperature")


def ctd(material, temp, extrapolate = False):
  """
    The code specified instantaneous CTD as a function of temperature

    Parameters:
      material:      the HBB class A material
      temp:          the temperature(s) to return values for, C

    Optional:
      extrapolate:   if true extrapolate properties
  """

  data=load_code_1D(material,"ctd")

  if extrapolate:
    ifn = inter.interp1d(data[:,0], data[:,1]*1.0e-6, fill_value = "extrapolate")
  else:
    ifn = inter.interp1d(data[:,0], data[:,1]*1.0e-6)

  try:
    return ifn(temp)
  except ValueError:
    raise errors.OutofRange("temperature")
