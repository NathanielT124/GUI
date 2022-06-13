#pylint: disable=missing-docstring
import unittest
from test.common import CommonCodeTableTests
import hbbdata.fatigue

class TestFatigueData(unittest.TestCase, CommonCodeTableTests):
  def setUp(self):
    self.forward = hbbdata.fatigue.strain_to_failure
    self.backward = hbbdata.fatigue.cycles_to_failure

    self.true_data = {
    # data in the row_l, col_l, val
        '304': [
        [1e1, 480, 0.0465],
        [4e2, 425, 0.00965],
        [1e3, 595, 0.0047],
        [2e3, 705, 0.00276],
        [4e4, 650, 0.00162]
        ],
        '316': [
        [2e1, 650, 0.0208],
        [4e2,  40, 0.0110],
        [1e3, 705, 0.00328],
        [4e4, 425, 0.00273],
        [1e5, 705, 0.00121],
        [1e6, 480, 0.00118]
        ],
        '2.25Cr-1Mo': [
        [2e2, 425, 0.0094],
        [1e3, 595, 0.0042],
        [2e4, 425, 0.0026],
        [1e5, 595, 0.00158],
        [4e5, 425, 0.00155],
        [1e6, 595, 0.00118]
        ],
        'gr91': [
        [2e1, 540, 0.019],
        [4e2, 540, 0.0062],
        [2e3, 540, 0.0044],
        [4e4, 540, 0.0021],
        [1e6, 540, 0.00163],
        [2e7, 540, 0.00132],
        [1e8, 540, 0.00120]
        ],
        '800H': [
        [1e1, 425, 0.05],
        [4e1, 760, 0.01233],
        [4e2, 540, 0.0066],
        [3e3, 425, 0.00644],
        [4e4, 760, 0.00164],
        [1e6, 425, 0.002]
        ],
        'A617': [
        [1e1, 425, 0.05007],
        [4e1, 704, 0.01156],
        [4e2, 950, 0.00279],
        [2e3, 871, 0.00278],
        [4e4, 425, 0.00340],
        [2e5, 950, 0.00082],
        [1e6, 704, 0.00135]
        ]
        }
