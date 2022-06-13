#pylint: disable=missing-docstring, invalid-name
import unittest
import numpy as np
from hbbdata.errors import OutofRange
from hbbdata.interaction import interaction_fatigue, interaction_creep, inside_envelope
from hbbdata.utility import load_code_1D

class TestAllInteraction(unittest.TestCase):
  def setUp(self):

    self.data_type = 'interaction'

    self.true_data = {
        '304': [0.3,0.3],
        '316': [0.3,0.3],
        '2.25Cr-1Mo': [0.1,0.1],
        'gr91': [0.1,0.01],
        '800H': [0.1,0.1],
        'A617': [0.1,0.1]
         }

    self.out_of_range = {'Df':[-0.1],
                        'Dc':[-0.1] }

    self.true_interpolated_values = {'800H':[[0.02, 0.82],
                                            [0.82, 0.02]] }

    self.true_inside_envelope = { 'True' :[[0.02, 0.81],[0.82,0.01]],
                                  'False':[[0.02, 0.83],[0.82,0.03]],
                                  'mat' : '800H' }


  def test_values(self):
    """
      Test all the interpolates against the references
    """
    for mat, data in self.true_data.items():
      s =     "\n ---------------------------------------------\n"
      s = s + "wrong interaction value for material {} \n" .format(mat)
      comp_value = load_code_1D(mat, self.data_type)

      self.assertTrue(np.array_equal(data, comp_value), s)


  def test_range(self):
    """
      Test all the interpolates against the references
    """
    material = '800H'
    for damage, data in self.out_of_range.items():
      if damage == 'Df':
        ifn = lambda D: interaction_fatigue(material, D)
      else:
        ifn = lambda D: interaction_creep(material, D)

      for d in data:
        with self.assertRaises(OutofRange):
          Dy = ifn(d) #pylint: disable=unused-variable

  def test_interaction_functions(self):
    """
      Test interaction_fatigue and interaction_creep
    """
    for mat, data in self.true_interpolated_values.items():
      for Df, Dc in data:
        DfInt = interaction_creep(mat, Dc)
        s =     "\n ---------------------------------------------\n"
        s = s  + "wrong value computed by interaction_creep \n"
        self.assertTrue(np.isclose(DfInt, Df), s)

        DcInt = interaction_fatigue(mat, Df)
        s =     "\n ---------------------------------------------\n"
        s = s  + "wrong value computed by interaction_fatigue \n"
        self.assertTrue(np.isclose(DcInt, Dc), s)

  def test_inside_envelope(self):
    """
      Test interaction_fatigue and interaction_creep
    """
    mat = self.true_inside_envelope['mat']
    del self.true_inside_envelope['mat']

    for flag, data in self.true_inside_envelope.items():
      for Df, Dc in data:
        if flag == 'True':
          realVal = True
        elif flag == 'False':
          realVal = False
        else:
          raise Exception('unknown flag for inside the envelope true data')

        compVal = inside_envelope(mat, Df, Dc)
        s =     "\n ---------------------------------------------\n"
        s = s  + "inside the envelope not working properly \n"
        self.assertTrue(np.equal(realVal, compVal), s)
