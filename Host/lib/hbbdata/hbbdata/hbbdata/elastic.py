"""
  This module returns the Code values of elastic properties as functions
  of temperature.
"""

import scipy.interpolate as inter

import hbbdata.errors as errors
from hbbdata.utility import load_code_1D

def poissons(material):
  """
    The ASME Poissons ratios are temperature independent so this function
    just returns the relevant value.

    Parameters:
      material:      the HBB class A material
  """
  errors.valid_mat(material)

# data validated 03-07-2017 by Andrea Rovinelli
  database = {'304': 0.31, '316': 0.31, '2.25Cr-1Mo': 0.30, 'gr91': 0.30,
      '800H': 0.31, 'A617': 0.31, 'A740H': 0.31}

  try:
    return database[material]
  except Exception:
    raise errors.MissingData(material)

def youngs(material, temp, extrapolate = False):
  """
    The code specifies the Young's modulus as a function of temperature

    Parameters:
      material:      the HBB class A material
      temp:          the temperature(s) to return values for, C
  """
  data = load_code_1D(material, "youngs")

  if extrapolate:
    ifn = inter.interp1d(data[:,0], data[:,1]*1000.0,
        fill_value = "extrapolate")
  else:
    ifn = inter.interp1d(data[:,0], data[:,1]*1000.0)

  try:
    return ifn(temp)
  except ValueError:
    raise errors.OutofRange("temperature")
