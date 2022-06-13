"""
  This module contains tools for the Section III, Division 5
  Elastic Perfectly Plastic (EPP) Code cases.
"""

import numpy as np
import scipy.interpolate as inter

import hbbdata.errors as errors
import hbbdata.plastic as plastic
import hbbdata.isochronous as isochronous
import hbbdata.utility as utility
from hbbdata import rupture
from hbbdata.limits import Sr_max_T

def pseudoyield_N862(material, t_prime, temp = np.linspace(20,600)):
  """
    The pseudoyield stress used in Code Case N-862

    Parameters:
      material:      HBB class A material
      t_prime:       trial life

    Optional:
      temp:          temperatures requested
  """
  #determine Kp from III.5.HBB-T-1411-1
  Kp = 0.9
  if material == 'gr91':
    Kp = 1.

  pseudo_yield = np.zeros_like(temp, dtype=float)
  for i, T in enumerate(temp):
    try:
      pseudo_yield[i] = min(plastic.yield_stress(material, T),
      rupture.S_r(material, T, t_prime, extrapolate = True) * Kp)
    except errors.OutofRange:
      if T <= Sr_max_T(material):
        pseudo_yield[i] = plastic.yield_stress(material, T)
      else:
        raise errors.OutofRange("temperature")

  return pseudo_yield

def pseudoyield_N861(material, life, target_strain,
    temp = np.linspace(40,600), disable_yield = False):
  """
    The EPP strain limits pseudoyield stress as a function of temperature

    Parameters:
      material:      HBB class A material
      life:          design life, in hours.  A life of 0 is interpreted to mean
                     use the hot tensile curve
      target_strain: the target strain

    Optional:
      temp:          temperature(s) to return
      disable_yield: if true skip the yield check
  """
  errors.valid_mat(material)

  vals = np.zeros(temp.shape)

  strains = np.linspace(0, target_strain+0.004)

  for i,temp_i in enumerate(temp):
    try:
      if np.isclose(life, 0):
        ic_strain, ic_stress = isochronous.hot_tensile(material, temp_i,
            strain = strains)
      else:
        ic_strain, ic_stress =  isochronous.isochronous(material, temp_i, life,
            strain = strains)

        eoff, soff = utility.offset(ic_strain, ic_stress) # pylint: disable=W0612

      ic_ifn = inter.interp1d(ic_strain, ic_stress)
      ival = ic_ifn(eoff + target_strain)
    except errors.OutofRange:
      ival = np.inf

    if not disable_yield:
      try:
        yval = plastic.yield_stress(material, temp_i)
      except errors.OutofRange:
        yval = np.inf

      if np.isinf(yval) and np.isinf(ival):
        raise errors.OutofRange("yield stress and isochronous")

      if yval < ival:
        vals[i] = yval
      else:
        vals[i] = ival
    else:
      vals[i] = ival

  if disable_yield:
    y_v = np.inf
    for v_i in vals:
      if not np.isinf(v_i):
        y_v = v_i
        break
    if np.isinf(y_v):
      raise errors.OutofRange("isochronous")
    for i, v_i in enumerate(vals):
      if np.isinf(v_i):
        vals[i] = y_v

  return temp, vals
