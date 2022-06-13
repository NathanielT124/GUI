#!/usr/bin/env python3

import numpy as np

import glob
import os.path
import re

if __name__ == "__main__":
  dirs = ["304", "316", "800H", "2.25Cr-1Mo", "gr91"]

  names = {"2.25Cr-1Mo": "2.25Cr-1Mo",
      "304": "304SS",
      "316": "316SS",
      "800H": "Alloy 800H",
      "gr91": "9Cr-1Mo-V"}

  for d in dirs:
    files = glob.glob(os.path.join(d, "*.png"))
    for f in files:
      T = int(os.path.basename(f).replace('.','-').split('-')[-2].strip('F'))
      print(".. figure:: %s" % os.path.join("figures",f))
      print("")
      print("\t Comparison between the current and implemented isochronous stress-strain curves for %s at %s°F." 
          % (names[d],T))
      print("")
