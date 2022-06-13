"""
  This module handles checks of the Code creep-fatigue interaction diagrams
"""

import numpy as np
import numpy.linalg as la

import hbbdata.errors as errors
from hbbdata.utility import load_code_1D

def dpoint_line(p1, p2, p):
  """
    Distance between a line segment defined by p1 and p2 and the point p

    Parameters:
      p1:        first line segment point
      p2:        second line segment point
      p:         point of interest
  """
  d = lambda x1, x2: la.norm(x2 - x1)

  l2 = d(p1, p2)**2.0
  if np.isclose(l2, 0.0):
    return d(p1, p)

  t = max(0, min(1, np.dot(p - p1, p2 - p1) / l2))
  proj = p1 + t * (p2 - p1)
  return d(p, proj)

def distance_envelope(material, damage_fatigue, damage_creep):
  """
    Distance from a point to the envelope, sign is positive if
    inside the envelop and negative if outside

    Parameters:
      material:          HBB Class A material
      damage_fatigue:    fatigue damage fraction
      damage_creep:      creep damage fraction
  """
  errors.valid_mat(material)

  if damage_fatigue < 0.0 or damage_creep < 0.0:
    raise errors.OutofRange("damage fraction")

  intersect=load_code_1D(material,"interaction")

  if inside_envelope(material, damage_fatigue, damage_creep):
    sgn = 1.0
  else:
    sgn = -1.0

  p = [damage_fatigue, damage_creep]

  return sgn * min(dpoint_line(np.array([0,1]), intersect, p),
      dpoint_line(intersect, np.array([1,0]), p))

def inside_envelope(material, damage_fatigue, damage_creep):
  """
    Return True if the point lies in the design envelope and False if not

    Parameters:
      material:          HBB Class A material
      damage_fatigue:    fatigue damage fraction
      damage_creep:      creep damage fraction
  """
  errors.valid_mat(material)

  if damage_fatigue < 0.0 or damage_creep < 0.0:
    raise errors.OutofRange("damage fraction")

  damage_creep_v = interaction_fatigue(material, damage_fatigue)

  return damage_creep <= damage_creep_v

def interaction_fatigue(material, damage_fatigue):
  """
    Enter the interaction diagram with a fatigue damage fraction and
    return the allowable creep damage fraction

    Parameters:
      material:             HBB Class A material
      damage_fatigue:       fatigue damage fraction
  """
  errors.valid_mat(material)

  if damage_fatigue < 0.0:
    raise errors.OutofRange("damage fraction")

  intersect=load_code_1D(material,"interaction")

  x_1 = 0.0
  y_1 = 1.0
  x_2 = intersect[0]
  y_2 = intersect[1]
  x_3 = 1.0
  y_3 = 0.0

  if damage_fatigue < x_2:
    return (y_2 - y_1) / (x_2 - x_1) * (damage_fatigue - x_1) + y_1

  return (y_3 - y_2) / (x_3 - x_2) * (damage_fatigue - x_2) + y_2

def interaction_creep(material, damage_creep):
  """
    Enter the interaction diagram with a creep damage fraction and return
    the allowable fatigue damage fraction

    Parameters:
      material:           HBB Class A material
      damage_creep:       creep damage fraction
  """
  errors.valid_mat(material)

  if damage_creep < 0.0:
    raise errors.OutofRange("damage fraction")

  intersect=load_code_1D(material,"interaction")

  x_1 = 0.0
  y_1 = 1.0
  x_2 = intersect[0]
  y_2 = intersect[1]
  x_3 = 1.0
  y_3 = 0.0

  if damage_creep > y_2:
    return (x_2 - x_1) / (y_2 - y_1) * (damage_creep - y_1) + x_1

  return (x_3 - x_2) / (y_3 - y_2) * (damage_creep - y_2) + x_2
