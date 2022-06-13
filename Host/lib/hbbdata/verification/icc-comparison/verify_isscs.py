#!/usr/bin/env python

import sys
sys.path.append('../..')
from hbbdata import isochronous

import numpy as np
import os.path
import matplotlib.pyplot as plt

def load_info(ref):
  di = os.path.dirname(ref)

  cases = {}

  with open(ref, 'r') as f:
    for line in f:
      if line.strip()[0] == "#":
        continue
      data = line.strip().split()
      
      fname = os.path.join(di, "%s_%iF.png" % (di, int(data[0])))
      T = float(data[0])
      strain = (float(data[1])/100.0, float(data[2])/100.0)
      stress = (float(data[3]), float(data[4]))
      times = map(float, data[5].split(','))

      cases[fname] = {"T": T, "strain": strain, "stress": stress, 
          "times": times}

  return cases

if __name__ == "__main__":
  materials = [ "304", "316", "800H", "2.25Cr-1Mo", "gr91"]
  materials = ["gr91"]

  for mat in materials:
    cases = load_info(os.path.join(mat, 'reference'))

    for img,data in cases.iteritems():
      fig, ax = plt.subplots()

      im = plt.imread(img)
      ax.imshow(im, extent = [data['strain'][0], data['strain'][1],
        data['stress'][0], data['stress'][1]], 
        aspect = 'auto')

      for t in data['times']:
        T = (data['T'] - 32.0) * 5.0 / 9.0
        if t == 0.0:
          strain, stress = isochronous.hot_tensile(mat, T, 
              np.linspace(0, data['strain'][1]))
        else:
          strain, stress = isochronous.isochronous(mat, T, 
              t, strain = np.linspace(0, data['strain'][1]))

        ax.plot(strain, stress, 'r-')
      
      plt.xlim(data['strain'][0], data['strain'][1])
      plt.ylim(data['stress'][0], data['stress'][1])

      plt.xlabel("Strain (mm/mm)")
      plt.ylabel("Stress (MPa)")
      plt.title("%s: %iF" % (mat, data['T']))
      plt.tight_layout()
      plt.show()
