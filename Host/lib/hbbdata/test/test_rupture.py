#pylint: disable=missing-docstring
import unittest
from test.common import CommonCodeTableTests
import hbbdata.rupture

class TestSrData(unittest.TestCase, CommonCodeTableTests):
  def setUp(self):
    self.forward = hbbdata.rupture.S_r
    self.backward = hbbdata.rupture.time_rupture

    self.true_data = {
    # data in the row_l, col_l, val
        '304': [
        [1e4, 425, 393],
        [1e2, 550, 254],
        [3e5, 650, 34],
        [1e4, 725, 34],
        [1e2, 800, 46]
        ],
        '316': [
        [3e5, 425, 445],
        [1e5, 550, 147],
        [3e1, 650, 199],
        [3e4, 725, 36],
        [1e1, 750, 125],
        [3e5, 800, 9]
        ],
        '2.25Cr-1Mo': [
        [1e4, 375, 396],
        [1e5, 425, 191],
        [1e2, 550, 150],
        [1e3, 600, 69],
        [3e1, 625, 94],
        [1e3, 650, 43]
        ],
        'gr91': [
        [3e5, 375, 487],
        [3e5, 425, 345],
        [1e1, 500, 374],
        [3e4, 575, 122],
        [1e2, 625, 130],
        [1e5, 650, 33]
        ],
        '800H': [
        [1e4, 450, 385],
        [1e5, 575, 113],
        [1e2, 675, 150],
        [3e4, 725, 40],
        [5e5, 800, 12],
        [3e1, 900, 38]
        ],
        'A617': [
        [1e5, 425, 564],
        [1e4, 525, 508],
        [1e3, 625, 314],
        [1e2, 775, 144],
        [3e1, 850, 103],
        [1e5, 925, 12]
        ]
        }
