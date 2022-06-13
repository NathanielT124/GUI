"""
  This module contains hbbdata specific errors
"""

class UnknownMaterial(ValueError):
  """
    Called if the user requests an unknown material.
  """
  def __init__(self, key):
    super(UnknownMaterial,self).__init__(
        "Unknown material %s not one of the HBB class A materials:"
        "304, 316, 2.25Cr-1Mo, gr91, 800H, A617, or A740H" % key)

class MissingData(ValueError):
  """
    Called if the requested table has not been digitized or otherwise doesn't
    exist.
  """
  def __init__(self, mat):
    super(MissingData,self).__init__("Missing data for material %s" % mat)

class OutofRange(ValueError):
  """
    Called if the user requests data outside the relevant Code table
  """
  def __init__(self, variable):
    super(OutofRange,self).__init__("A supplied %s is out of range" % variable)

class ColumnOutofRange(ValueError):
  """
    Call if the user requests data out of the relevant 2D Code table
  """
  def __init__(self, val):
    super(ColumnOutofRange,self).__init__(
        "The provided column value %f is greater than the column headers."
        % val)

def valid_mat(material):
  """
    The current list of valid materials.
  """
  if material not in ['304', '316', '2.25Cr-1Mo', 'gr91', '800H', 'A617',
      'A740H']:
    raise UnknownMaterial(material)

class LabelValueNotPresent(ValueError):
  """
    Called in testing if the requested data label isn't actually in the table
  """
  def __init__(self, mat):
    super(LabelValueNotPresent,self).__init__(
        "***** Missing label value for %s *****" % mat)

class FunctionNotBounded(ValueError):
  """
    Called in testing if the function fails to extrapolate when requested
  """
  def __init__(self, funcName):
    super(FunctionNotBounded,self).__init__(
        "***** Wrong behavior!!! %s allows for extrapolation" % funcName)
