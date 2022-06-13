"""
  Module contains various utility functions for reading and processing
  data from the Code tables.
"""

import os
import numpy as np
import scipy.interpolate as inter
import scipy.optimize as opt

import hbbdata.errors as errors

BASEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')

def get_allowable_time(data, temp, value, extrapolate = True, logx = True):
  """
    Get a time corresponding to an allowable stress,
    returning the minimum or maximum value if your are off the chart

    Parameters:
      data:          table data
      temp:          temperature
      extrapolate:   extrapolate off table
      stress:        desired stress value
      tmin:          minimum time
      tmax:          maximum time
      ztol:          tolerance on answer
  """
  times = data[0]
  temps = data[1]
  datas = np.array(data[2])

  if temp < temps[0] or temp > temps[-1]:
    raise ValueError("Temperature falls outside chart for inverse determination")

  # Figure out which row you lie between
  if np.isclose(temp, temps[0]):
    vals = datas[0,:]
  elif np.isclose(temp, temps[-1]):
    vals = datas[-1,:]
  else:
    ind = np.searchsorted(temps, temp)
    w1 = (temps[ind] - temp) / (temps[ind]-temps[ind-1])
    w2 = 1.0 - w1
    vals = w1*datas[ind-1,:]+w2*datas[ind,:]

  # Check to see if you're in a flat region
  if np.isclose(value, vals[0]):
    iargs = np.argsort(vals)
    ind = np.searchsorted(np.sort(vals), value,
        side = 'right')
    ind = iargs[ind-1]
    return times[ind]

  if logx:
    xfn = np.log10
    ixfn = lambda xx: 10.0**xx
  else:
    xfn = lambda xx: xx
    ixfn = lambda xx: xx

  if extrapolate:
    ifn = inter.interp1d(vals, xfn(times), fill_value = "extrapolate")
  else:
    ifn = inter.interp1d(vals, xfn(times))

  return ixfn(ifn(value))

def extrap2d(x, y, z):
  """
    Regrettably scipy documentation lies and interp2d won't actually
    extrapolate outside the domain.

    This function repairs that behavior.

    Parameters:
      x:         x points
      y:         y points
      z:         z points

    Note this does "Code table" type interpolation where the x-axis value is
    interpolated first (usually temperature) and then the y-axis
  """
  bfn = inter.interp2d(x, y, z)

  def ifn(x_i, y_i):
    """
      2D interpolation to fixed data
    """
    if y_i < y[0] or y_i > y[-1]:
      raise errors.OutofRange("extrap2d 2D axis")
    new_z = [float(bfn(xj, y_i)) for xj in x]
    new_ifn = inter.interp1d(x, new_z, bounds_error = False,
        fill_value = "extrapolate")
    return float(new_ifn(x_i))

  return ifn

def offset(strain, stress, offset_val = 0.2/100.0):
  """
    Find the offset strain and stress from curves

    Parameters:
      strain:        strain values
      stress:        stress values

    Optional:
      offset_val:    offset to use
  """
  ifn = inter.interp1d(strain, stress)
  E = stress[1] / strain[1]

  x = opt.brentq(lambda x: E*x - E * offset_val - ifn(x), 0, np.max(strain))

  return x, ifn(x)

def bilinear_interpolate(data, x, y, logx = False, logy = False, logdata = False,
    extrapolate = False, inf = 1e6):
  """
    Do bilinear interpolation over a fixed grid

    Parameters:
      data:      tuple of (xheaders, yheaders, data)
      x:         x point you want
      y:         y point you want

    Optional:
      logx:          Do log-linear interpolation for x
      logy:          Do log-linear interpolation for y
      logdata:       Do log-linear interpolation over the data
      extrapolate:   extrapolate outside the table
      inf:           value to use for zero if log interpolate is on
  """
  if logx:
    x_labels = np.log10(data[0])
    if x > 0.0:
      x = np.log10(x)
    else:
      x = -inf
  else:
    x_labels = data[0]

  if logy:
    y_labels = np.log10(data[1])
    if y > 0.0:
      y = np.log10(y)
    else:
      y = -inf
  else:
    y_labels = data[1]

  if logdata:
    z_data = np.array(data[2])
    bad = z_data <= 0.0
    z_data[np.logical_not(bad)] = np.log10(z_data[np.logical_not(bad)])
    z_data[bad] = -inf
    trans = lambda z: 10.0**z
  else:
    z_data = np.array(data[2])
    trans = lambda z: z

  if extrapolate:
    ifn = extrap2d(x_labels, y_labels, z_data)
    return trans(ifn(x,y))

  ifn = inter.interp2d(x_labels, y_labels, z_data,
      bounds_error = True)
  return float(trans(ifn(x,y)))

def max_col_interpolate(data, colv, y, log = False,
    extrapolate = False, inf = 1e6, use_close = False):
  """
    Extrapolate linearly (or log linearly) based on a maximum
    column value

    Parameters:
      data:          tuple of (xheaders, yheaders, data)
      colv:          column value to select, usecol max st. colv < usecol
      y:             point to interpolate to

    Optional:
      log:           use log linear interpolation
      extrapolate:   extrapolate off the table
      inf:           value to use for zero if log interpolate is on
      use_close:     if you exceed the max temperature raise an error, unless
                     this is set
  """
  if log:
    labels = np.log10(data[1])
    if y > 0.0:
      y = np.log10(y)
    else:
      y = -inf
  else:
    labels = data[1]

  slabels = data[0]

  inds = np.where(slabels >= np.array(colv))[0]
  if len(inds) == 0 and use_close:
    i = len(slabels) - 1
  elif len(inds) == 0:
    raise errors.ColumnOutofRange(colv)
  else:
    i = np.min(inds) #I'm not sure that where always return ascending results

  dint = np.array(data[2])[:,i]

  if extrapolate:
    ifn = inter.interp1d(labels, dint, fill_value = "extrapolate")
  else:
    ifn = inter.interp1d(labels, dint)

  return float(ifn(y))


def load_code_table(material, data_kind):
  """
    Load in a Code table from a file

    Parameters:
      material:     the name of the material
      data_kind:    the kind of tabulated data to load (fatigue, Sr, ...)

    Returns horizontal labels, vertical labels, and data
  """

  errors.valid_mat(material)
  dpath = os.path.join(BASEDIR, 'data', data_kind, material)

  x_labels = []
  y_labels = []
  data = []

  try:
    with open(dpath, 'r') as f:
      for i,row in enumerate(f):
        if row.strip() == "": # Skip blank lines
          continue
        if row[0] == '#': # Skip comments
          continue
        line = list(map(float, row.strip().split()))
        if i == 0:
          x_labels = line
        else:
          y_labels.append(line[0])
          data.append(line[1:])
  except:
    raise errors.MissingData(material)

  return x_labels, y_labels, data


def load_code_1D(material, data_kind): # pylint: disable=C0103
  """
    load 1D code tables

    Parameters:
      material:      the HBB class A material
      data_kind:     directory name containing the data
  """
  errors.valid_mat(material)
  dpath = os.path.join(BASEDIR, 'data', data_kind, material)
  try:
    data = np.loadtxt(dpath)
  except Exception:
    raise errors.MissingData(material)

  return data

def memoize(fn):
  """
    Helper to memoize values of common functions

    Parameters:
      fn:       function to memoize
  """
  memo = {}
  def helper(*args, **kwargs):
    """
      Memoize function
    """
    uargs = args + tuple(kwargs.values())
    if uargs not in memo:
      memo[uargs] = fn(*args, **kwargs)
    return memo[uargs]

  return helper
