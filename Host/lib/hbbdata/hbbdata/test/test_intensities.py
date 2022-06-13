#pylint: disable=missing-docstring
import unittest
import numpy as np
from hbbdata import intensities

class TestSo(unittest.TestCase):
  def setUp(self):
    self.true_data = {
        '304':
        [
          [425, 105],
          [450, 102],
          [475, 101],
          [500, 99 ],
          [525, 86 ],
          [550, 74 ],
          [575, 69 ],
          [600, 65 ],
          [625, 51 ],
          [650, 42 ],
          [675, 34 ],
          [700, 27 ],
          [725, 21 ],
          [750, 17 ],
          [775, 14 ],
          [800, 11 ]
        ],
        '316':
        [
          [425, 110],
          [450, 108],
          [475, 108],
          [500, 107],
          [525, 101],
          [550, 88 ],
          [575, 77 ],
          [600, 76 ],
          [625, 62 ],
          [650, 51 ],
          [675, 39 ],
          [700, 30 ],
          [725, 23 ],
          [750, 18 ],
          [775, 13 ],
          [800, 11 ]
        ],
        '2.25Cr-1Mo':
        [
          [375, 123],
          [400, 123],
          [425, 116],
          [450, 116],
          [475, 99 ],
          [500, 81 ],
          [525, 64 ],
          [550, 48 ],
          [575, 35 ],
          [600, 26]
        ],
        'gr91':
        [
          [375, 184],
          [400, 178],
          [425, 172],
          [450, 165],
          [475, 154],
          [500, 133],
          [525, 117],
          [550, 102],
          [575, 81 ],
          [600, 62 ],
          [625, 46 ],
          [650, 29 ]
        ],
        '800H':
        [
          [425, 105],
          [450, 104],
          [475, 103],
          [500, 101],
          [525, 99 ],
          [550, 89 ],
          [575, 74 ],
          [600, 68 ],
          [625, 62 ],
          [650, 51 ],
          [675, 41 ],
          [700, 34 ],
          [725, 28 ],
          [750, 23 ]
        ],
        'A617':
        [
          [425, 148],
          [450, 147],
          [475, 146],
          [500, 145],
          [525, 144],
          [550, 144],
          [575, 144],
          [600, 143],
          [625, 142],
          [650, 124],
          [675, 101],
          [700, 81 ],
          [725, 64 ],
          [750, 50 ],
          [775, 40 ],
          [800, 31 ],
          [825, 25 ],
          [850, 19 ],
          [875, 15 ],
          [900, 12 ],
          [925, 10 ],
          [950, 7.9]
        ]}

  def test_intensity(self):
    for mat, data in self.true_data.items():
      for temp, actual in data:
        comp = intensities.S_o(mat, temp)
        self.assertTrue(np.isclose(actual, comp), 
            "S_o for material %s does not agree at temperature %f (%f vs. %f)" %
            (mat, temp, actual, comp))

class TestSmt(unittest.TestCase):
  """
    We are relying on this test to check Sm as well, as the Code only
    tabulates Smt
  """
  def setUp(self):
    self.true_data = {'800H': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0, 300000.0], [425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0, 675.0, 700.0, 725.0, 750.0], [[105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0], [104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 104.0], [103.0, 103.0, 103.0, 103.0, 103.0, 103.0, 103.0, 103.0, 103.0, 103.0, 103.0], [101.0, 101.0, 101.0, 101.0, 101.0, 101.0, 101.0, 101.0, 101.0, 101.0, 101.0], [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 98.0], [99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 94.0, 88.0], [98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 94.0, 82.0, 72.0], [97.0, 97.0, 97.0, 97.0, 97.0, 97.0, 96.0, 91.0, 79.0, 67.0, 58.0], [96.0, 96.0, 96.0, 96.0, 96.0, 96.0, 92.0, 80.0, 68.0, 59.0, 50.0], [95.0, 95.0, 95.0, 95.0, 95.0, 84.0, 73.0, 62.0, 53.0, 45.0, 39.0], [93.0, 93.0, 93.0, 93.0, 84.0, 71.0, 60.0, 51.0, 44.0, 37.0, 31.0], [91.0, 91.0, 91.0, 82.0, 70.0, 59.0, 50.0, 41.0, 35.0, 29.0, 25.0], [85.0, 85.0, 81.0, 69.0, 58.0, 49.0, 41.0, 34.0, 30.0, 24.0, 20.0], [78.0, 77.0, 69.0, 58.0, 49.0, 40.0, 34.0, 28.0, 24.0, 20.0, 16.0]]], '304': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0, 300000.0], [425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0, 675.0, 700.0, 725.0, 750.0, 775.0, 800.0], [[105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0], [102.0, 102.0, 102.0, 102.0, 102.0, 102.0, 102.0, 102.0, 102.0, 102.0, 102.0], [101.0, 101.0, 101.0, 101.0, 101.0, 101.0, 101.0, 101.0, 101.0, 101.0, 101.0], [99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 93.0], [98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 87.0, 73.0], [96.0, 96.0, 96.0, 96.0, 96.0, 96.0, 96.0, 94.0, 82.0, 70.0, 58.0], [93.0, 93.0, 93.0, 93.0, 93.0, 93.0, 91.0, 78.0, 66.0, 56.0, 46.0], [91.0, 91.0, 91.0, 91.0, 91.0, 89.0, 75.0, 63.0, 54.0, 44.0, 37.0], [89.0, 89.0, 89.0, 89.0, 87.0, 74.0, 62.0, 51.0, 43.0, 36.0, 29.0], [88.0, 88.0, 88.0, 84.0, 73.0, 61.0, 51.0, 42.0, 35.0, 28.0, 23.0], [85.0, 85.0, 83.0, 77.0, 61.0, 51.0, 42.0, 35.0, 28.0, 22.0, 19.0], [82.0, 80.0, 69.0, 61.0, 50.0, 42.0, 34.0, 28.0, 23.0, 18.0, 15.0], [77.0, 70.0, 61.0, 52.0, 43.0, 35.0, 29.0, 22.0, 18.0, 15.0, 12.0], [69.0, 60.0, 52.0, 44.0, 36.0, 29.0, 23.0, 18.0, 15.0, 12.0, 9.0], [61.0, 51.0, 44.0, 36.0, 29.0, 24.0, 19.0, 15.0, 12.0, 9.0, 7.0], [53.0, 43.0, 37.0, 29.0, 23.0, 18.0, 15.0, 11.0, 9.0, 7.0, 5.0]]], '316': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0, 300000.0], [425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0, 675.0, 700.0, 725.0, 750.0, 775.0, 800.0], [[110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0], [108.0, 108.0, 108.0, 108.0, 108.0, 108.0, 108.0, 108.0, 108.0, 108.0, 108.0], [107.0, 107.0, 107.0, 107.0, 107.0, 107.0, 107.0, 107.0, 107.0, 107.0, 107.0], [106.0, 106.0, 106.0, 106.0, 106.0, 106.0, 106.0, 106.0, 106.0, 106.0, 106.0], [105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0], [104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 101.0, 87.0], [104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 104.0, 95.0, 79.0, 67.0], [102.0, 102.0, 102.0, 102.0, 102.0, 102.0, 102.0, 91.0, 75.0, 62.0, 51.0], [101.0, 101.0, 101.0, 101.0, 101.0, 94.0, 86.0, 72.0, 59.0, 48.0, 40.0], [101.0, 101.0, 101.0, 98.0, 84.0, 72.0, 64.0, 57.0, 48.0, 38.0, 31.0], [98.0, 98.0, 98.0, 80.0, 69.0, 58.0, 51.0, 44.0, 38.0, 30.0, 24.0], [95.0, 91.0, 78.0, 65.0, 54.0, 46.0, 41.0, 34.0, 28.0, 22.0, 18.0], [90.0, 75.0, 63.0, 52.0, 44.0, 36.0, 31.0, 25.0, 21.0, 16.0, 13.0], [82.0, 62.0, 51.0, 41.0, 35.0, 29.0, 24.0, 19.0, 16.0, 11.0, 9.0], [70.0, 50.0, 40.0, 32.0, 27.0, 23.0, 18.0, 14.0, 12.0, 8.0, 7.0], [61.0, 40.0, 32.0, 25.0, 21.0, 17.0, 13.0, 10.0, 8.0, 5.0, 4.0]]], 'gr91': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0, 300000.0], [375.0, 400.0, 425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0], [[183.0, 183.0, 183.0, 183.0, 183.0, 183.0, 183.0, 183.0, 183.0, 183.0, 183.0], [179.0, 179.0, 179.0, 179.0, 179.0, 179.0, 179.0, 179.0, 179.0, 179.0, 179.0], [172.0, 172.0, 172.0, 172.0, 172.0, 172.0, 172.0, 172.0, 172.0, 172.0, 172.0], [165.0, 165.0, 165.0, 165.0, 165.0, 165.0, 165.0, 165.0, 165.0, 165.0, 165.0], [156.0, 156.0, 156.0, 156.0, 156.0, 156.0, 156.0, 156.0, 156.0, 156.0, 154.0], [147.0, 147.0, 147.0, 147.0, 147.0, 147.0, 147.0, 147.0, 147.0, 138.0, 131.0], [136.0, 136.0, 136.0, 136.0, 136.0, 136.0, 136.0, 132.0, 126.0, 115.0, 106.0], [125.0, 125.0, 125.0, 125.0, 125.0, 125.0, 121.0, 111.0, 102.0, 93.0, 85.0], [114.0, 114.0, 114.0, 114.0, 114.0, 108.0, 99.0, 90.0, 81.0, 73.0, 66.0], [101.0, 101.0, 101.0, 101.0, 97.0, 86.0, 80.0, 71.0, 63.0, 54.0, 48.0], [88.0, 88.0, 88.0, 86.0, 78.0, 70.0, 63.0, 54.0, 44.0, 36.0, 30.0], [76.0, 76.0, 76.0, 69.0, 62.0, 54.0, 44.0, 36.0, 29.0, 22.0, 17.0]]], '2.25Cr-1Mo': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0, 300000.0], [375.0, 400.0, 425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0], [[None, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0], [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0], [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 112.0], [122.0, 122.0, 122.0, 122.0, 122.0, 122.0, 122.0, 122.0, 116.0, 101.0, 89.0], [119.0, 119.0, 119.0, 119.0, 119.0, 119.0, 114.0, 106.0, 92.0, 80.0, 71.0], [116.0, 116.0, 116.0, 116.0, 116.0, 111.0, 99.0, 85.0, 74.0, 64.0, 56.0], [112.0, 112.0, 112.0, 106.0, 97.0, 89.0, 78.0, 66.0, 57.0, 48.0, 41.0], [107.0, 107.0, 98.0, 89.0, 81.0, 74.0, 64.0, 54.0, 46.0, 38.0, 33.0], [100.0, 89.0, 80.0, 72.0, 66.0, 59.0, 50.0, 42.0, 35.0, 29.0, 25.0], [89.0, 72.0, 66.0, 59.0, 53.0, 47.0, None, None, None, None, None], [72.0, 58.0, 53.0, 49.0, 42.0, 36.0, None, None, None, None, None], [62.0, 43.0, 42.0, 41.0, 35.0, 28.0, None, None, None, None, None]]], 'A617': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0], [425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0, 675.0, 700.0, 725.0, 750.0, 775.0, 800.0, 825.0, 850.0, 875.0, 900.0, 925.0, 950.0], [[148.0, 148.0, 148.0, 148.0, 148.0, 148.0, 148.0, 148.0, 148.0, 148.0], [148.0, 148.0, 148.0, 148.0, 148.0, 148.0, 148.0, 148.0, 148.0, 148.0], [146.0, 146.0, 146.0, 146.0, 146.0, 146.0, 146.0, 146.0, 146.0, 146.0], [146.0, 146.0, 146.0, 146.0, 146.0, 146.0, 146.0, 146.0, 146.0, 146.0], [145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0], [145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0], [145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0], [145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 130.0], [145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 125.0, 105.0], [145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 145.0, 121.0, 102.0, 84.0], [145.0, 145.0, 145.0, 145.0, 145.0, 142.0, 119.0, 98.0, 82.0, 67.0], [145.0, 145.0, 145.0, 145.0, 142.0, 116.0, 97.0, 79.0, 65.0, 52.0], [145.0, 145.0, 145.0, 141.0, 117.0, 95.0, 78.0, 63.0, 51.0, 41.0], [145.0, 145.0, 144.0, 117.0, 95.0, 76.0, 62.0, 50.0, 41.0, 33.0], [145.0, 136.0, 119.0, 95.0, 77.0, 61.0, 50.0, 40.0, 32.0, 26.0], [124.0, 121.0, 98.0, 77.0, 62.0, 49.0, 40.0, 32.0, 26.0, 20.0], [112.0, 99.0, 80.0, 63.0, 51.0, 40.0, 32.0, 25.0, 20.0, 16.0], [99.0, 82.0, 65.0, 51.0, 41.0, 32.0, 26.0, 20.0, 16.0, 13.0], [87.0, 67.0, 53.0, 42.0, 33.0, 26.0, 21.0, 16.0, 13.0, 10.0], [74.0, 55.0, 44.0, 34.0, 27.0, 21.0, 16.0, 13.0, 10.0, 8.0], [62.0, 45.0, 36.0, 27.0, 22.0, 17.0, 13.0, 10.0, 8.0, 6.0], [50.0, 37.0, 29.0, 22.0, 18.0, 13.0, 11.0, 8.0, 6.0, 5.0]]]}

  def test_intensity(self, tol = 3.0):
    """
      Clearly the Code is a bit "rounding challenged" so ignore differences 
      <= 3 MPa

      There is also a list of "ignore" values

      Several values are wrong in the code, so we accept the
      calculated values.  We've initiated code action to fix them
    """
    ignore = [
        ("800H", 1, 725),
        ("800H", 1, 750),
        ("800H", 10000, 625),
        ("800H", 30000, 625),
        ("800H", 100000, 625),
        ("A617", 1, 775),
        ("gr91", 10000, 525),
        ("2.25Cr-1Mo", 3000, 475),
        ("304", 100, 675),
        ("316", 1, 725),
        ("316", 1, 750),
        ("316", 1, 775),
        ("316", 1, 800),
        ("316", 30, 675)
        ]

    def ignore_me(mat, time, temp):
      for m, t, T in ignore:
        if (mat == m) and (time == t) and (temp == T):
          return True
      
      return False

    die = False
    for mat, data in self.true_data.items():
      for j, time in enumerate(data[0]):
        for i, temp in enumerate(data[1]):
          
          if ignore_me(mat, time, temp):
            continue

          actual = data[2][i][j]
          if actual is None:
            continue
          else:
            comp = round(intensities.S_mt(mat, temp, time, 
              no_reduction = True))

            if np.abs(comp-actual) > tol:
              die = True
              print("S_mt for material %s does not agree at time = %f and"
                " temperature %f (%f vs. %f)" % (mat, time, temp, actual, 
                  comp))

    self.assertFalse(die)


class TestSt(unittest.TestCase):
  def setUp(self):
    self.true_data = {'800H': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0, 300000.0], [425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0, 675.0, 700.0, 725.0, 750.0], [[132.0, 132.0, 132.0, 132.0, 132.0, 132.0, 132.0, 132.0, 132.0, 132.0, 132.0], [130.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0], [129.0, 129.0, 129.0, 129.0, 129.0, 129.0, 128.0, 128.0, 128.0, 127.0, 126.0], [128.0, 128.0, 128.0, 128.0, 128.0, 128.0, 127.0, 126.0, 126.0, 125.0, 124.0], [126.0, 126.0, 126.0, 126.0, 126.0, 125.0, 124.0, 124.0, 122.0, 119.0, 109.0], [124.0, 124.0, 124.0, 124.0, 124.0, 123.0, 122.0, 121.0, 113.0, 103.0, 88.0], [123.0, 123.0, 123.0, 122.0, 121.0, 120.0, 117.0, 111.0, 96.0, 83.0, 72.0], [121.0, 121.0, 120.0, 119.0, 117.0, 114.0, 107.0, 91.0, 79.0, 67.0, 58.0], [119.0, 118.0, 116.0, 115.0, 109.0, 102.0, 89.0, 75.0, 64.0, 55.0, 47.0], [117.0, 115.0, 112.0, 109.0, 101.0, 85.0, 74.0, 62.0, 53.0, 45.0, 39.0], [114.0, 109.0, 105.0, 98.0, 85.0, 72.0, 61.0, 52.0, 44.0, 37.0, 31.0], [110.0, 100.0, 94.0, 82.0, 70.0, 59.0, 50.0, 41.0, 35.0, 29.0, 25.0], [99.0, 88.0, 82.0, 70.0, 58.0, 49.0, 41.0, 34.0, 29.0, 24.0, 20.0], [94.0, 80.0, 69.0, 58.0, 49.0, 40.0, 34.0, 28.0, 24.0, 20.0, 16.0]]], '304': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0, 300000.0], [425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0, 675.0, 700.0, 725.0, 750.0, 775.0, 800.0], [[141.0, 141.0, 141.0, 141.0, 141.0, 141.0, 141.0, 141.0, 141.0, 141.0, 141.0], [138.0, 138.0, 138.0, 138.0, 138.0, 138.0, 138.0, 138.0, 138.0, 137.0, 134.0], [136.0, 136.0, 135.0, 135.0, 135.0, 134.0, 132.0, 130.0, 129.0, 126.0, 116.0], [133.0, 133.0, 132.0, 131.0, 128.0, 125.0, 123.0, 121.0, 117.0, 107.0, 93.0], [130.0, 129.0, 127.0, 122.0, 118.0, 115.0, 113.0, 108.0, 100.0, 87.0, 73.0], [126.0, 125.0, 121.0, 115.0, 110.0, 107.0, 103.0, 94.0, 82.0, 70.0, 58.0], [123.0, 121.0, 116.0, 110.0, 105.0, 100.0, 91.0, 78.0, 66.0, 56.0, 46.0], [120.0, 115.0, 109.0, 102.0, 97.0, 88.0, 75.0, 63.0, 54.0, 44.0, 37.0], [116.0, 107.0, 101.0, 93.0, 87.0, 74.0, 62.0, 51.0, 43.0, 36.0, 29.0], [110.0, 98.0, 92.0, 84.0, 73.0, 61.0, 51.0, 42.0, 35.0, 28.0, 23.0], [102.0, 90.0, 83.0, 72.0, 61.0, 51.0, 42.0, 35.0, 28.0, 22.0, 19.0], [93.0, 80.0, 71.0, 61.0, 50.0, 42.0, 34.0, 28.0, 23.0, 18.0, 15.0], [86.0, 70.0, 61.0, 52.0, 43.0, 35.0, 29.0, 22.0, 18.0, 15.0, 12.0], [78.0, 60.0, 52.0, 44.0, 36.0, 29.0, 23.0, 18.0, 15.0, 12.0, 9.0], [69.0, 51.0, 44.0, 36.0, 29.0, 24.0, 19.0, 15.0, 12.0, 9.0, 7.0], [60.0, 43.0, 37.0, 29.0, 23.0, 18.0, 15.0, 11.0, 9.0, 7.0, 5.0]]], '316': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0, 300000.0], [425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0, 675.0, 700.0, 725.0, 750.0, 775.0, 800.0], [[143.0, 143.0, 143.0, 143.0, 143.0, 143.0, 143.0, 143.0, 143.0, 143.0, 143.0], [142.0, 142.0, 142.0, 142.0, 142.0, 142.0, 142.0, 142.0, 142.0, 142.0, 140.0], [141.0, 141.0, 141.0, 141.0, 141.0, 141.0, 141.0, 141.0, 140.0, 138.0, 135.0], [140.0, 140.0, 140.0, 140.0, 140.0, 139.0, 139.0, 138.0, 134.0, 131.0, 125.0], [138.0, 138.0, 138.0, 138.0, 138.0, 136.0, 134.0, 130.0, 126.0, 118.0, 108.0], [136.0, 136.0, 135.0, 134.0, 132.0, 128.0, 125.0, 119.0, 113.0, 101.0, 87.0], [133.0, 133.0, 131.0, 127.0, 124.0, 119.0, 114.0, 105.0, 95.0, 79.0, 67.0], [131.0, 129.0, 126.0, 121.0, 116.0, 110.0, 105.0, 91.0, 75.0, 62.0, 51.0], [127.0, 121.0, 118.0, 111.0, 103.0, 94.0, 86.0, 72.0, 59.0, 48.0, 40.0], [123.0, 116.0, 108.0, 97.0, 84.0, 72.0, 64.0, 57.0, 48.0, 38.0, 31.0], [118.0, 106.0, 94.0, 80.0, 69.0, 58.0, 51.0, 44.0, 38.0, 30.0, 24.0], [112.0, 91.0, 78.0, 65.0, 54.0, 46.0, 41.0, 34.0, 28.0, 22.0, 18.0], [101.0, 75.0, 63.0, 52.0, 44.0, 36.0, 31.0, 25.0, 21.0, 16.0, 13.0], [88.0, 62.0, 51.0, 41.0, 35.0, 29.0, 24.0, 19.0, 16.0, 11.0, 9.0], [74.0, 50.0, 40.0, 32.0, 27.0, 23.0, 18.0, 14.0, 12.0, 8.0, 7.0], [61.0, 40.0, 32.0, 25.0, 21.0, 17.0, 13.0, 10.0, 8.0, 5.0, 4.0]]], 'gr91': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0, 300000.0], [375.0, 400.0, 425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0], [[325.0, 325.0, 325.0, 325.0, 325.0, 325.0, 325.0, 325.0, 325.0, 325.0, 325.0], [317.0, 317.0, 317.0, 317.0, 317.0, 317.0, 316.0, 316.0, 307.0, 290.0, 275.0], [307.0, 307.0, 307.0, 307.0, 307.0, 307.0, 292.0, 276.0, 262.0, 246.0, 232.0], [294.0, 294.0, 294.0, 294.0, 279.0, 264.0, 249.0, 234.0, 220.0, 206.0, 193.0], [275.0, 275.0, 271.0, 256.0, 241.0, 225.0, 211.0, 197.0, 184.0, 171.0, 160.0], [262.0, 249.0, 235.0, 219.0, 205.0, 191.0, 178.0, 165.0, 153.0, 141.0, 131.0], [242.0, 214.0, 200.0, 185.0, 172.0, 163.0, 148.0, 136.0, 126.0, 115.0, 106.0], [217.0, 182.0, 170.0, 156.0, 144.0, 132.0, 119.0, 111.0, 102.0, 93.0, 85.0], [189.0, 154.0, 142.0, 130.0, 119.0, 108.0, 99.0, 90.0, 81.0, 73.0, 66.0], [164.0, 126.0, 115.0, 107.0, 97.0, 86.0, 79.0, 71.0, 63.0, 54.0, 48.0], [139.0, 106.0, 96.0, 86.0, 78.0, 70.0, 62.0, 54.0, 44.0, 36.0, 30.0], [117.0, 87.0, 78.0, 69.0, 62.0, 54.0, 47.0, 36.0, 29.0, 22.0, 17.0]]], '2.25Cr-1Mo': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0, 300000.0], [375.0, 400.0, 425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0], [[None, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0], [243.0, 243.0, 239.0, 231.0, 224.0, 216.0, 205.0, 196.0, 183.0, 172.0, 161.0], [241.0, 230.0, 220.0, 211.0, 200.0, 186.0, 173.0, 160.0, 142.0, 125.0, 112.0], [226.0, 207.0, 197.0, 186.0, 176.0, 164.0, 149.0, 130.0, 116.0, 101.0, 89.0], [206.0, 183.0, 170.0, 159.0, 147.0, 136.0, 122.0, 106.0, 92.0, 80.0, 71.0], [182.0, 156.0, 144.0, 132.0, 122.0, 111.0, 99.0, 85.0, 74.0, 64.0, 56.0], [153.0, 127.0, 116.0, 106.0, 97.0, 89.0, 78.0, 66.0, 57.0, 48.0, 41.0], [131.0, 108.0, 98.0, 89.0, 81.0, 74.0, 64.0, 54.0, 46.0, 38.0, 33.0], [109.0, 89.0, 80.0, 72.0, 66.0, 59.0, 50.0, 42.0, 35.0, 29.0, 25.0], [89.0, 72.0, 66.0, 59.0, 53.0, 47.0, None, None, None, None, None], [72.0, 58.0, 53.0, 49.0, 42.0, 36.0, None, None, None, None, None], [62.0, 43.0, 42.0, 41.0, 35.0, 28.0, None, None, None, None, None]]], 'A617': [[1.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0], [425.0, 450.0, 475.0, 500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0, 675.0, 700.0, 725.0, 750.0, 775.0, 800.0, 825.0, 850.0, 875.0, 900.0, 925.0], [[245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0], [245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0, 245.0], [242.0, 242.0, 242.0, 242.0, 242.0, 242.0, 242.0, 242.0, 242.0, 242.0], [240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0], [238.0, 238.0, 238.0, 238.0, 238.0, 238.0, 238.0, 238.0, 238.0, 238.0], [235.0, 235.0, 235.0, 235.0, 235.0, 235.0, 235.0, 235.0, 235.0, 200.0], [234.0, 234.0, 234.0, 234.0, 234.0, 234.0, 234.0, 225.0, 192.0, 161.0], [233.0, 233.0, 233.0, 233.0, 233.0, 233.0, 218.0, 182.0, 155.0, 130.0], [232.0, 232.0, 232.0, 232.0, 232.0, 210.0, 178.0, 148.0, 125.0, 105.0], [231.0, 231.0, 231.0, 231.0, 208.0, 173.0, 145.0, 121.0, 102.0, 84.0], [231.0, 231.0, 231.0, 205.0, 172.0, 142.0, 119.0, 98.0, 82.0, 67.0], [231.0, 231.0, 207.0, 170.0, 142.0, 116.0, 97.0, 79.0, 65.0, 52.0], [231.0, 208.0, 173.0, 141.0, 117.0, 95.0, 78.0, 63.0, 51.0, 41.0], [231.0, 174.0, 144.0, 117.0, 95.0, 76.0, 62.0, 50.0, 41.0, 33.0], [219.0, 146.0, 119.0, 95.0, 77.0, 61.0, 50.0, 40.0, 32.0, 26.0], [185.0, 121.0, 98.0, 77.0, 62.0, 49.0, 40.0, 32.0, 26.0, 20.0], [156.0, 99.0, 80.0, 63.0, 51.0, 40.0, 32.0, 25.0, 20.0, 16.0], [130.0, 82.0, 65.0, 51.0, 41.0, 32.0, 26.0, 20.0, 16.0, 13.0], [108.0, 67.0, 53.0, 42.0, 33.0, 26.0, 21.0, 16.0, 13.0, 10.0], [90.0, 55.0, 44.0, 34.0, 27.0, 21.0, 16.0, 13.0, 10.0, 8.0], [75.0, 45.0, 36.0, 27.0, 22.0, 17.0, 13.0, 10.0, 8.0, 6.0]]]}

  def test_intensity(self):
    die = False
    for mat, data in self.true_data.items():
      for j, time in enumerate(data[0]):
        for i, temp in enumerate(data[1]):
          actual = data[2][i][j]
          if actual is None:
            continue
          else:
            comp = round(intensities.S_t(mat, temp, time))

            if not np.isclose(comp, actual):
              die = True
              print("S_t for material %s does not agree at time = %f and"
                " temperature %f (%f vs. %f)" % (mat, time, temp, actual, 
                  comp))

    self.assertFalse(die)
