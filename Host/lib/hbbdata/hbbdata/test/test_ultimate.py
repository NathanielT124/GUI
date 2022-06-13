#pylint: disable=missing-docstring
import unittest
from test.common import Common1dTest
import hbbdata.plastic

class TestAllUltimate(unittest.TestCase, Common1dTest):
  def setUp(self):
    self.getter = hbbdata.plastic.ultimate_tensile_stress

    self.true_data = {
        '304': [
          [-30,517],
          [200,442],
          [300,437],
          [425,433],
          [525,402],
          [550,388],
          [600,355],
          [700,264],
          [800,159]
          ],
        '316': [
          [-30,517],
          [200,496],
          [300,495],
          [475,474],
          [525,450],
          [550,435],
          [600,396],
          [700,288],
          [800,149]
          ],
        '2.25Cr-1Mo': [
          [-30,414],
          [200,401],
          [475,401],
          [525,384],
          [550,358],
          [600,290],
          [650,202]
          ],
        'gr91': [
          [-30,586],
          [100,586],
          [300,577],
          [400,534],
          [525,410],
          [550,379],
          [600,303],
          [650,228]
          ],
        '800H': [
          [-30,448],
          [200,446],
          [350,440],
          [475,439],
          [525,432],
          [550,402],
          [725,282],
          [900,109]
          ],
        'A617': [
          [-30,655],
          [200,655],
          [350,635],
          [475,611],
          [525,603],
          [550,593],
          [725,470],
          [900,221],
          [950,151]
          ]
          }


    self.too_high = {
        '304': [801.0, 950.0],
        '316': [801.0, 950.0],
        '2.25Cr-1Mo': [651, 850.0],
        'gr91': [651.0, 850.0],
        '800H': [901.0, 1000.0],
        'A617': [951.0, 1050.0]
        }

    self.too_low = {
        '304': [-31, -100],
        '316': [-31, -100],
        '2.25Cr-1Mo': [-31, -100],
        'gr91': [-31, -100],
        '800H': [-31, -100],
        'A617': [-31, -100]
        }
