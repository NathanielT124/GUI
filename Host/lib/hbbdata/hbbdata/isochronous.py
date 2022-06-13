#pylint: disable=C0103, too-many-statements, too-many-lines, no-member, no-self-use, arguments-differ
"""
  This module returns values for isochronous and hot tensile curves for the
  Code materials.
"""

import numpy as np
import scipy.interpolate as inter
import scipy.optimize as opt
import scipy.integrate as inte

import hbbdata.errors as errors
from hbbdata import elastic

class CurveModel(object):
  """
    Base class of all the models for isochronous curve generation.

    Takes care of common tasks like summing strains and inverting
    equations
  """
  def tensile(self, stress, T):
    """
      The sum of elastic + plastic strain

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    return self.elastic(stress, T) + self.plastic(stress, T)

  def total(self, stress, T, time):
    """
      The sum of elastic + plastic + creep strain

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
        time:       time, in hrs
    """
    return self.tensile(stress, T) + self.creep(stress, T, time)

  def hot_tensile(self, strain, T):
    """
      Generate a point on the hot tensile curve

      Parameters:
        strain:     nominal engineering strain
        T:          temperature in C

      Keyword parameters:
        lb:         lower bound for the Brentq bracket
        ub:         upper bound for the Brentq bracket
    """
    sfn = lambda x: strain - self.tensile(x, T)
    try:
      return opt.brentq(sfn, self.lb, self.ub)
    except ValueError:
      return opt.newton(sfn, (self.lb+self.ub)/2.0)

  def isochronous(self, strain, T, time):
    """
      Generate a point on the isochronous curve

      Parameters:
        strain:     nominal engineering strain
        T:          temperature in C
        time:       time in hours

      Keyword parameters:
        lb          lower bound for the Brentq bracket
        ub          upper bound for the Brentq bracket
    """
    sfn = lambda x: strain - self.total(x, T, time)
    return opt.brentq(sfn, self.lb, self.ub)

class Blackburn(CurveModel):
  """
    The Blackburn equations do the hot tensile curves in true strain
  """
  def tensile(self, stress, T):
    """
      The sum of elastic + plastic strain

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    if stress == 0.0:
      return 0.0

    return self.elastic(stress, T) + self.plastic(stress, T)

class Model316H(Blackburn):
  """
    The 316H Blackburn model
  """
  def __init__(self, *args, **kwargs):
    super(Model316H,self).__init__(*args, **kwargs)
    self.lb = 0.0
    self.ub = 215.0

  def elastic(self, stress, T):
    """
      The elastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    Tk = T + 273.15
    E = (3.3675e7 - 13823 *Tk) * 0.00689476 # Blackburn in psi

    return stress / E

  def plastic(self, stress, T):
    """
      The plastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    Tk = T + 273.15

    A = 1.25
    sy = A * (23402.6 - 8.04798 * Tk) * 0.00689476 # psi to MPa
    sp = sy + (-8188.8 + 3.51356 * Tk) * 0.00689476 # psi to MPa

    K1 = (60786.5 - 13.7959 * Tk) * 0.00689476 # psi to MPa
    m1 = 0.309503 + 6.13276e-5 * Tk # Already unitless

    if stress < sp:
      return 0.0
    elif Tk <= 1088.8 and Tk >= 588:
      return ((stress-sp)/K1)**(1.0/m1)
    else:
      raise errors.OutofRange("temperature")

  def creep(self, stress, T, time):
    """
      The creep strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
        time:       time, in hours
    """
    Tk = T + 273.15
    TF = (Tk - 273.15) * 9.0/5.0 + 32.0
    stress_psi = stress / 0.00689476

    # Oh god why
    if (TF >= 799.0) and (TF <1000.0):
      G = 0.0
      H = 0.0
      D = 5.7078e13
      beta = -4.257e-4 + 7.733e-7 * Tk
      n = 4.6
      C = 7.1
      B = 5.7078e13
      L = np.exp(43.1255) * np.exp(-49995.0/Tk)
      A = 5.6229e12
      Q = 67000.0
      R = 1.987
    elif (TF >= 1000.0) and (TF < 1075.0):
      G = 1.28221 - 1.58103e-3 * Tk
      H = -3.20553e-4 + 3.95256e-7 * Tk
      D = -4.4989e17 + 5.54768e14 * Tk
      beta = -4.257e-4 + 7.733e-7 * Tk
      n = -80.9236 + 0.105455 * Tk
      C = 25.5318 - 0.0227273 * Tk
      B = -3.92183e16 + 4.84416e13 * Tk

      z = Tk - 610.0
      M = -1153.38 + 16.4457 * z - 0.0754331 * z**2.0 + 0.000107956 * z**3.0
      L = np.exp(M)

      A = -7.85348e15 + 9.69329e12 * Tk
      Q = 67000
      R = 1.987
    elif (TF >= 1075.0) and (TF < 1100.0):
      G = 1.28221 - 1.58103e-3 * Tk
      H = -3.20553e-4 + 3.95256e-7 * Tk
      D = 2.86941e17 - 3.09286e14 * Tk
      beta = -4.257e-4 + 7.733e-7 * Tk
      n = 50.1136 - 0.0482143 * Tk
      C = 25.5318 - 0.0227273 * Tk
      B = 1.44225e-8 * np.exp(45475.8 / Tk)

      z = Tk - 610
      M = -274.235 + 1.15596 * z - 0.00115945 * z**2.0
      L = np.exp(M)
      A = 5.28787e-6 * np.exp(39057.1 / Tk)
      Q = 67000
      R = 1.987
    elif (TF >= 1100.0) and (TF <= 1200.0):
      G = -0.271855 + 2.13509e-4 * Tk
      H = 6.79633e-5 - 5.33787e-8 * Tk
      D = 2.86941e17 - 3.09286e14 * Tk
      beta = -4.257e-4 + 7.733e-7 * Tk
      n = 50.1136 - 0.0482143 * Tk
      C = 54.5625 - 0.05625 * Tk
      B = 1.44225e-8 * np.exp(45475.8/Tk)

      z = Tk - 610
      M = -274.235 + 1.15598 * z - 0.00115945 * z**2.0
      L = np.exp(M)

      A = 5.28787e-6 * np.exp(39057.1 / Tk)
      Q = 67000.0
      R = 1.987
    elif (TF >= 1200.0) and (TF < 1300.0):
      G = -0.692411 + 6.69643e-4 * Tk
      H = 1.73103e-4 - 1.67411e-7 * Tk
      D = 1.3369e10 * np.exp(10878.5/Tk)
      beta = -4.257e-4 + 7.733e-7 * Tk
      n = 14.4647 - 9.54954e-3 * Tk
      C = 7.68378 - 5.4054e-3 * Tk
      B = 2.85517e8 * np.exp(10878.5/Tk)

      w = Tk - 680
      M = -54.6029 + 0.118486*w - 8.63568e-6 * w**2.0
      L = np.exp(M)

      A = 6.03371e10 * np.exp(4967.76 / Tk)
      Q = 67000
      R = 1.987
    elif (TF >= 1300.0) and (TF <= 1500.0):
      G = -0.704318 + 6.61818e-4 * Tk
      H = 1.7608e-4 - 1.70455e-7 * Tk
      D = 1.3369e10 * np.exp(10878.5/Tk)
      beta = -4.257e-4 + 7.733e-7 * Tk
      n = 14.4647 - 9.54954e-3 * Tk
      C = 7.68378 - 5.4054e-3 * Tk
      B = 2.85517e8 * np.exp(10878.5/Tk)

      w = Tk - 680
      M = -54.6029 + 0.118486*w - 8.63568e-6 * w**2.0
      L = np.exp(M)

      A = 6.03371e10 * np.exp(4967.76/Tk)
      Q = 67000
      R = 1.987
    else:
      raise errors.OutofRange("temperature")

    scrit = 4000.0

    if stress == 0.0:
      return 0.0

    if stress_psi < scrit:
      ex = 0.0
    else:
      ex = G + H * stress_psi

    s = max(D*np.sinh(beta*stress_psi/n)**n * np.exp(-Q/(R*Tk)), 2.5e-2)
    r = max(B*np.sinh(beta*stress_psi/n)**n * np.exp(-Q/(R*Tk)), L*stress_psi**(n-3.6))

    edm = A * np.sinh(beta*stress_psi/n)**n * np.exp(-Q/(R*Tk))
    et = C * edm / r

    return (ex * (1 - np.exp(-s*time)) + et * (1-np.exp(-r*time)) +
        edm * time) / 100.0 # % to nominal

class Model304H(Blackburn):
  """
    The 304H Blackburn model
  """
  def __init__(self, *args, **kwargs):
    super(Model304H,self).__init__(*args, **kwargs)
    self.lb = 0.0
    self.ub = 800.0

  def elastic(self, stress, T):
    """
      The elastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    Tk = T + 273.15
    E = (3.3675e7 - 13823.0 * Tk) * 0.00689476 # Blackburn in ipsi

    return stress / E

  def plastic(self, stress, T):
    """
      The plastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    Tk = T + 273.15

    A = 1.25
    sy = A * (25850.5 - 12.8179 * Tk) * 0.00689476
    sp = sy + (-12198.0 + 6.7093 * Tk) * 0.00689476

    K1 = (69964.0 - 25.4491 * Tk) * 0.00689476
    m1 = 0.25824 + 7.749e-5 * Tk

    if stress < sp:
      return 0.0
    elif T <= 1088.8:
      return ((stress-sp)/K1)**(1.0/m1)
    else:
      raise errors.OutofRange("temperature")

  def creep(self, stress, T, time):
    """
      The creep strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
        time:       time, in hours
    """
    Tk = T + 273.15
    TF = (Tk - 273.15) * 9.0/5.0 + 32.0
    stress_psi = stress / 0.00689476

    if (TF >= 799) and (TF < 850):
      G = 0.0
      H = 0.0
      D = 2.266e15
      beta_r = -2.252e-4 + 5.401e-7 * Tk
      n_r = 3.5
      C = 2.469e-3 * np.exp(6580.986 / Tk)
      B = 2.518e13
      A = 1.38e13
      beta_e = -3.652e-4 + 7.518e-7 * Tk
      n_e = 6.0
      Q = 67000.0
      R = 1.987
    elif (TF >= 850) and (TF <= 1000):
      G = 2.24449 - 3.08547e-3 * Tk
      H = -3.74081e-4 + 5.14244e-7 * Tk
      D = 2.266e15
      beta_r = -2.252e-4 + 5.401e-7 * Tk
      n_r = 3.5
      C = 2.469e-3 * np.exp(6580.986 / Tk)
      B = 2.518e13
      A = 1.38e13
      beta_e = -3.652e-4 + 7.518e-7 * Tk
      n_e = 6.0
      Q = 67000.0
      R = 1.987
    elif (TF > 1000) and (TF < 1100):
      G = -0.257143
      H = 4.28571e-5
      D = 3.19663e16*np.exp(-3.66218e-3*Tk)
      beta_r = -2.252e-4 + 5.401e-7 * Tk
      n_r = 3.5
      C = 56.2405-5.91691e-2*Tk
      B = 2.518e13
      A = 1.38e13
      beta_e = -3.652e-4 + 7.518e-7 * Tk
      n_e = 6.0
      Q = 67000.0
      R = 1.987
    elif (TF >= 1100) and (TF <= 1500):
      G = -0.257143
      H = 4.28571e-5
      D = 2.518e14
      beta_r = -2.252e-4 + 5.407e-7 * Tk
      n_r = 3.5
      C = 5.0
      B = 2.518e13
      A = 1.38e13
      beta_e = -3.652e-4 + 7.518e-7 * Tk
      n_e = 6.0
      Q = 67000.0
      R = 1.987
    else:
      raise errors.OutofRange("temperature")

    scrit = 6000.0

    if np.isclose(stress_psi, 0.0):
      return 0.0

    if stress_psi < scrit:
      ex = 0.0
    else:
      ex = G + H * stress_psi

    s = D*np.sinh(beta_r*stress_psi/n_r)**n_r * np.exp(-Q/(R*Tk))
    r = B*np.sinh(beta_r*stress_psi/n_r)**n_r * np.exp(-Q/(R*Tk))

    edm = A * np.sinh(beta_e*stress_psi/n_e)**n_e * np.exp(-Q/(R*Tk))
    et = C * edm / r

    return (ex * (1.0 - np.exp(-s*time)) + et * (1-np.exp(-r*time)) + edm * time) / 100.0

class ModelGr91(CurveModel):
  """
    Swindeman's Grade 91 model
  """
  def __init__(self, *args, **kwargs):
    super(ModelGr91,self).__init__(*args, **kwargs)
    self.lb = 0.0
    self.ub = 800.0

  def elastic(self, stress, T):
    """
      The elastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    Td = np.array([371,399,427,454,482,500,510,538,550,566,593,600,621,649])
    Ed = np.array([188,184,180,175,170,166,163,157,150,149,141,139,133,125]) * 1000.0
    E = inter.interp1d(Td, Ed)

    if (T < Td[0]) or (T > Td[-1]):
      raise errors.OutofRange("temperature")

    return stress / E(T)

  def plastic(self, stress, T, e_inf = 1.0):
    """
      The plastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C

      Keyword Parameters:
        e_inf:      large strain value to return if the stress exceeds the UTS
    """
    Td = np.array([371,399,427,454,482,500,510,538,550,566,593,600,621,649])
    Pd = np.array([317,310,303,296,283,269,262,228,207,186,145,138,110,83])
    Ud = np.array([603,586,569,541,507,483,469,431,410,386,338,324,283,234])
    bd = np.array([3.73,4.49,4.77,5.88,8.24,9.30,10.59,14.11,15.70,17.36,14.84,14.80,14.70,10.97])
    Yd = np.array([483,479,469,459,445,431,421,393,410,355,303,296,252,200])

    TY1d = Td[1:]
    Y1d = np.array([358,350,336,319,307,298,273,262,245,214,206,183,152])

    P = inter.interp1d(Td, Pd)
    U = inter.interp1d(Td, Ud)
    b = inter.interp1d(Td, bd)
    Y = inter.interp1d(Td, Yd)
    Y1 = inter.interp1d(TY1d, Y1d, fill_value = "extrapolate")

    if (T < Td[0]) or (T > Td[-1]):
      raise errors.OutofRange("temperature")

    R = 1.25 * Y1(T) / Y(T)

    if stress > U(T) * R:
      return e_inf
    elif stress > P(T) * R:
      return ((np.log((P(T) * R - U(T) * R) / (stress - U(T) * R)))**2.0 / b(T)) / 100.0
    return 0.0

  def creep(self, stress, T, time):
    """
      The creep strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
        time:       time, in hours
    """
    if (T < 371) or (T > 650):
      raise errors.OutofRange("temperature")

    if T < 482:
      D = 847000.0
    elif T >= 537:
      D = 5450000.0
    else:
      D = (T - 482) * (5450000.0 - 847000.0) / (538.0 - 482.0) + 847000.0

    if T < 537:
      Q0 = 25330.0
    else:
      Q0 = 23260.0

    V0 = 0.023
    C = 2.25e22
    n = 5.0
    V = 0.038
    Q = 77280.0

    Tk = T + 273.15

    return (D * stress * np.exp(V0 * stress) * np.exp(-Q0 / Tk) * time **(1.0/3.0
        ) + C * stress**n * np.exp(V * stress) * np.exp(-Q / Tk) * time) / 100.0

class ModelA617(CurveModel):
  """
    Messner's A617 model
  """
  def __init__(self, *args, **kwargs):
    super(ModelA617,self).__init__(*args, **kwargs)
    self.lb = 0.0
    self.ub = 800.0

  def elastic(self, stress, T):
    """
      The elastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    E = elastic.youngs("A617", T)

    return stress / E

  def plastic(self, stress, T, e_inf = 1.0):
    """
      The plastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C

      Keyword Parameters:
        e_inf:      large strain value to return if the stress exceeds the UTS
    """
    if T < 425.0 or T > 955.0:
      raise errors.OutofRange("temperature")

    if stress == 0.0:
      return 0.0

    if T > 750.0:
      Ts = [750,800, 850, 900, 955]
      Sos = [228,178,50,51,54]
      Sus = [522,317,214,164,122]
      ds = [9.70,35.5,482,1250,1240]

      So_fn = inter.interp1d(Ts, Sos)
      Su_fn = inter.interp1d(Ts, Sus)
      d_fn = inter.interp1d(Ts, ds)

      So = So_fn(T)
      Su = Su_fn(T)
      d = d_fn(T)

      if stress < So:
        return 0.0
      elif stress > Su:
        return e_inf
      return -np.log(1.0 - (stress - So) / (Su - So)) / d
    else:
      Ts = [425, 450, 500, 550, 600, 650, 700, 750]
      s0s = [175, 170, 166, 165, 178, 209, 206, 205]
      Ks = [0.056, 0.053, 0.050, 0.052, 0.067, 0.13, 0.12, 0.093]
      ns = [1.96, 1.97, 2.01, 1.84, 1.50, 2.13, 2.29, 1.55]
      s0_fn = inter.interp1d(Ts, s0s)
      K_fn = inter.interp1d(Ts, Ks)
      n_fn = inter.interp1d(Ts, ns)

      s0 = s0_fn(T)
      K = K_fn(T)
      n = n_fn(T)

      if stress < s0:
        return 0.0
      return K * ((stress - s0)/s0)**n

  def creep(self, stress, T, time):
    """
      The creep strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
        time:       time, in hours
    """
    A = -4.480
    B1 = -3.174
    B2 = -2.510
    T0 = 775.0
    eps0 = 1.656e7

    kboltz = 1.38064e-23 * 1000.0
    b = 2.019 * 1.0e-7

    mu = lambda T: elastic.youngs("A617", T) /   (2 * (1.0 + elastic.poissons("A617")))

    Ta = T + 273.15

    if T <= T0:
      B = B2
    else:
      B = B1

    return eps0 * np.exp(mu(T)*B*b**3.0/(A * kboltz * Ta)) * (
        stress / mu(T))**(-mu(T) * b**3.0 / (A * kboltz * Ta)) * time

class Model800H(CurveModel):
  """
    The reconstructed 800H model
  """
  def __init__(self, *args, **kwargs):
    super(Model800H,self).__init__(*args, **kwargs)
    self.lb = 0.0
    self.ub = 800.0

  def elastic(self, stress, T):
    """
      The elastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    if T < 426.0 or T > 761.0:
      raise errors.OutofRange("temperature")

    E = elastic.youngs("800H", T, extrapolate = True) # Need to get from 750 to 761

    return stress / E

  def plastic(self, stress, T, lb = 1.0e-10, ub = 1.0):
    """
      The plastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C

      Keyword Parameters:
        lb:         lower bound for Brent's method
        ub:         upper bound for Brent's method
    """
    if T < 426.0 or T > 761.0:
      raise errors.OutofRange("temperature")

    if stress == 0.0:
      return 0.0

    def strain_to_stress(ep):
      """
        Take strain to stress
      """
      # Need temperature in Rankine
      Tr = (T *1.8) + 491.67

      # coefficients of the 4th order polynomials
      B1c = [  3.18312201e+00,  -1.94465649e-01, -2.53179862e-02,  7.99351461e-02, -4.54091288e-02]
      B2c = [1.72297330e-01,  -6.54008012e-04,  2.66280150e-02, -9.36658919e-02,  5.86915202e-02]
      B3c = [3.75671539e-02,   1.32897986e-02, -2.96225929e-02,  6.14678657e-03,  5.12025443e-03]
      B4c = [4.50390345e-03,   4.98519009e-03,  4.82573850e-02, -1.01054504e-01,  5.47052447e-02]

      T_min = 1259.67
      T_max = 1859.67

      Delta_t = T_max-T_min

      B1f = lambda x: (B1c[0] + B1c[1]*((x-T_min)/Delta_t)
          + B1c[2]*((x-T_min)/Delta_t)**2
          + B1c[3]*(((x-T_min)/Delta_t)**3)
          + B1c[4]*(((x-T_min)/Delta_t)**4))
      B2f = lambda x: (B2c[0] + B2c[1]*((x-T_min)/Delta_t)
          + B2c[2]*((x-T_min)/Delta_t)**2
          + B2c[3]*(((x-T_min)/Delta_t)**3)
          + B2c[4]*(((x-T_min)/Delta_t)**4))
      B3f = lambda x: (B3c[0] + B3c[1]*((x-T_min)/Delta_t)
          + B3c[2]*((x-T_min)/Delta_t)**2 + B3c[3]*(((x-T_min)/Delta_t)**3)
          + B3c[4]*(((x-T_min)/Delta_t)**4))
      B4f = lambda x: (B4c[0] + B4c[1]*((x-T_min)/Delta_t)
          + B4c[2]*((x-T_min)/Delta_t)**2 + B4c[3]*(((x-T_min)/Delta_t)**3)
          + B4c[4]*(((x-T_min)/Delta_t)**4))

      #this model wants strain in percentage
      epu = ep * 100

      return (np.exp(B1f(Tr) + B2f(Tr) * np.log(epu)
        + B3f(Tr) * np.log(epu)**2.0 + B4f(Tr) * np.log(epu)**3.0) * 6.895)

    ee = self.elastic(stress, T)

    if stress < strain_to_stress(ee):
      return 0.0
    sfn = lambda e: stress - strain_to_stress(e)
    return opt.brentq(sfn, lb, ub) - ee

  def creep(self, stress, T, time):
    """
      The creep strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
        time:       time, in hours
    """
    if T < 426.0 or T > 761.0:
      raise errors.OutofRange("temperature")

    if (stress == 0.0) or (time == 0.0):
      return 0.0

    u1 = -1.84503305e+04
    u2 =  1.09662615e+04
    u3 = -4.62117596e+00
    u4 =  1.77459417e+05
    u5 = -6.75590904e+01

    Tr = (T+273.15)*1.8 # Rankine

    Sk = stress/6.895

    T1 = u1/Tr
    T2 = u2/Tr+u3
    T3 = u4/Tr+u5

    return np.exp((np.log(time) - T1 * np.log(Sk) - T3) / T2) / 100.0

class ModelA740H(CurveModel):
  """
    Made up A740H curves
  """
  def __init__(self, *args, **kwargs):
    super(ModelA740H,self).__init__(*args, **kwargs)
    self.lb = 0.0
    self.ub = 800.0

  def elastic(self, stress, T):
    """
      The elastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    E = elastic.youngs("A740H", T)
    return stress / E

  def plastic(self, stress, T, e_inf = 1.0):
    """
      The plastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    if T < 600 or T > 850:
      raise errors.OutofRange("temperature")

    if T <= 800.0:
      s0 = inter.interp1d([600,700,725,750,775,800],
          [400.24,400.24,374.20,348.16,312.255,276.35])(T)
      K = 10.0**(inter.interp1d([600,700,725,750,775,800],
        np.log10([0.0704,0.0704,0.0357,0.0181,0.0055,0.0017]))(T))
      n = inter.interp1d([600,700,725,750,775,800],
          [6.6480,6.6480,7.1315,7.6150,10.971,14.327])(T)

      if stress < s0:
        return 0.0
      else:
        return K*((stress-s0)/s0)**n

    else:
      sp = inter.interp1d([800,825,850],[574.991,521.631,468.271])(T)
      s1 = inter.interp1d([800,825,850],[455.850,319.315,182.780])(T)
      d = inter.interp1d([800,825,850],[908.324,2212.205,3516.087])(T)

      if stress < s1:
        return 0.0
      elif stress > sp:
        return e_inf
      else:
        return -np.log(1.0 - (stress - s1) / (sp - s1)) / d

  def creep(self, stress, T, time):
    """
      The creep strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
        time:       time, in hours
    """
    eps0 = 1.19e10
    k = 1.38064e-20
    b = 2.53e-7
    A = -10.98557
    B = -0.53098

    E = elastic.youngs("A740H", T)
    nu = elastic.poissons("A740H")
    mu = E / (2.0 * (1 + nu))

    return eps0 * np.exp(B * mu * b**3.0 / (A * k * (T + 273.15 ))
        ) * (stress / mu) ** (-mu * b**3.0 / (A * k * (T+273.15))) * time

class Model225Cr(CurveModel):
  """
    Booker's 2.25Cr-1Mo model
  """
  def __init__(self, *args, **kwargs):
    super(Model225Cr,self).__init__(*args, **kwargs)
    self.lb = 0.0
    self.ub = 800.0

  def elastic(self, stress, T):
    """
      The elastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
    """
    if T < 371 or T > 649:
      raise errors.OutofRange("temperature")

    E = elastic.youngs("2.25Cr-1Mo", T)

    return stress / E

  def plastic(self, stress, T, e_inf = 1.0):
    """
      The plastic strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C

      Keyword Parameters:
        e_inf:      big strain value to return if you're above
                    the UTS
    """
    if T < 371 or T > 649:
      raise errors.OutofRange("temperature")

    if stress == 0.0:
      return 0.0

    temps = [371, 399, 427, 454, 482, 510, 538, 566, 593, 621, 649]
    sYs = [210.26110788,193.41696677,199.53334023,194.17852203,
        183.83060583,180.77609127,183.2855386,173.75745429,169.39649398,
        153.29557145,133.87945406]
    Bs = [576.81250335,541.04380868,477.98193045,487.8576125,601.36801303,
        418.50675089,389.22730052,317.15988506,300.7890696,277.60111266,
        239.8507004]
    Cs = [-25.5946613,-32.08696447,-39.89889061,-35.38462892,-26.44939313,
        -45.34906153,-40.45340962,-60.25435782,-52.15993414,-58.78196275,
        -65.16805611]

    sY_fn = inter.interp1d(temps, sYs)
    B_fn = inter.interp1d(temps, Bs)
    C_fn = inter.interp1d(temps, Cs)

    sY = sY_fn(T)
    B = B_fn(T)
    C = C_fn(T)
    A = sY - B

    if stress < sY:
      return 0.0
    elif stress > B:
      return e_inf
    return 1.0 / C * np.log((stress - B) / A)

  def creep(self, stress, T, time):
    """
      The creep strain as a function of stress and temperature

      Parameters:
        stress:     stress, in MPa
        T:          temperature, in C
        time:       time, in hours
    """
    if T < 371 or T > 649:
      raise errors.OutofRange("temperature")

    if T <= 372:
      return 0.0

    if stress == 0.0 or time == 0.0:
      return 0

    Tu = [20,50,100,150,200,250,300,350,400,450,500,550,600, 621, 650]
    Uu = [508,486,464,455,456,462,469,473,468,452,418,364,284, 300.0, 269.0]
    Ufn = inter.interp1d(Tu, Uu)

    Tk = T + 273.15
    U = Ufn(T)

    tIa = 10.0**(-13.528 + 6.5196*U/Tk + 23349.0/Tk - 5693.8/Tk * np.log10(stress))
    tIb = 10.0**(-11.098 - 4.0951*stress/U + 11965.0/Tk)

    if T <= 454:
      tI = tIa
    elif T > 510:
      tI = tIb
    else:
      tI = inter.interp1d([454,510],[tIa,tIb])(T)

    C = 10.0**(1.0328 + 168680.0 / (Tk * U) - 0.023772 * U + 0.0079141 * U * np.log10(stress))
    p = 10.0**(7.6026 + 3.3396 * np.log10(stress) - 12323.0 / Tk)
    em = 10.0**(6.7475 + 0.011426 * stress + 987.72 / U * np.log10(stress) - 13494.0 / Tk)

    Cp = 10.0**(-0.051086 + 140730.0 / (Tk * U) - 0.01 * U + 0.0037345 * U * np.log10(stress))
    pp = 10.0**(8.1242 + 0.0179678 * stress + 404.63 / U * np.log10(stress) - 11659.0 / Tk)
    emp = 10.0**(11.498 - 8.2226 * U / Tk - 20448.0 / Tk + 5862.4 / Tk * np.log10(stress))

    e1 = (C * p * time / (1.0 + p * time) + em * time)
    e2 = (Cp * pp * time / (1.0 + pp * time) + emp * time)

    if e2 < e1:
      return e2 / 100.0
    if time < tI:
      return (C * p * time / (1.0 + p * time) + em * time) / 100.0
    eI = (C * p * tI / (1.0 + p * tI) + em * tI)
    tc = ((-emp - Cp * pp + eI * pp
      + np.sqrt(4.0 * eI * emp * pp +
        (emp + (Cp - eI) * pp)**2.0)) / (2.0 * emp * pp))

    tp = time - (tI - tc)

    return (Cp * pp * tp / (1.0 + pp * tp) + emp * tp) / 100.0

def select_obj(material):
  """
    Select the proper ISSC object

    Parameters:
      material:      which HBB class A material
  """
  errors.valid_mat(material)

  if material == '316':
    obj = Model316H()
  elif material == '304':
    obj = Model304H()
  elif material == 'gr91':
    obj = ModelGr91()
  elif material == 'A617':
    obj = ModelA617()
  elif material == '800H':
    obj = Model800H()
  elif material == '2.25Cr-1Mo':
    obj = Model225Cr()
  elif material == 'A740H':
    obj = ModelA740H()
  else:
    raise errors.MissingData(material)

  return obj

def isochronous(material, temperature, life, strain = np.linspace(0,0.022)):
  """
    Supply the isochronous curve at the provided temperature and design life.

    Parameters:
      material:      HBB class A material
      temperature:   temperature, in C
      life:          design life, in hours

    Optional:
      strain:        nominal engineering strains to return
  """
  obj = select_obj(material)

  stress = np.array([obj.isochronous(e, temperature, life) for e in strain])

  return strain, stress

def hot_tensile(material, temperature, strain = np.linspace(0,0.022)):
  """
    Supply the hot tensile curve at the requested temperature

    Parameters:
      material:      HBB class A material
      temperature:   temperature, in C

    Optional:
      strain:        nominal engineering strains to return
  """
  obj = select_obj(material)

  stress = np.array([obj.hot_tensile(e, temperature) for e in strain])

  return strain, stress

def time_from_temp_stress_strain(material, temperature, stress, strain,
    min_t = 0.0, max_t = 300000.0):
  """
    Calculate the time corresponding to a given temperature, stress, and strain.

    Parameters:
      material:     HBB class A material
      temperature:  temperature, in C
      time:         stress, in MPa
      strain:       strain, mm/mm

    Optional:
      min_t         minimum value of time to bracket, default 0
      max_t         maximum value of time to bracket, default 300,000

  """
  obj = select_obj(material)

  fn = lambda t: obj.total(stress, temperature, t) - strain

  return opt.brentq(fn, min_t, max_t)

def strain_to_time_stress(material, temperature, time, stress):
  """
    Calculate the strain at a given temperature, time and stress

    Parameters:
      material:      HBB class A material
      temperature:   temperature, in C
      time:          time, in hours
      stress:        stress, in MPa
  """
  obj = select_obj(material)

  return obj.total(stress, temperature, time)

def issc_relaxation_analysis_stress(material, temperature, stress, times):
  """
    Perform a code method of isochronous curves relaxation analysis
    hitting each of the indicated times.

    This routine is stress-based

    Parameters:
      material:      HBB class A material
      temperature:   temperature, in C
      stress:        initial stress, in MPa
      times:         times to solve for, in hours
  """
  obj = select_obj(material)

  return issc_relaxation_analysis_strain(material, temperature,
      obj.tensile(stress, temperature), times)

def issc_relaxation_analysis_strain(material, temperature, strain, times):
  """
    Perform a code method of isochronous curves relaxation analysis
    hitting each of the indicated times.

    This routine is strain-based

    Parameters:
      material:      HBB class A material
      temperature:   temperature, in C
      strain:        initial strain, mm/mm
      times:         times to solve for, in hours
  """
  obj = select_obj(material)

  if np.isclose(times[0], 0.0):
    stress = [obj.hot_tensile(strain, temperature)]
  else:
    stress = [obj.isochronous(strain, temperature, times[0])]
  stress += [obj.isochronous(strain, temperature, t) for t in times[1:]]

  return np.array(stress)

def relaxation_analysis_rate(material, temperature, stress, times, dt = 0.1):
  """
    Perform a relaxation analysis starting from the indicated stress
    using the creep equation underlying the ISSC to calculate the
    relaxation profile.

    Parameters:
      material      HBB material
      temperature   temperature, in C
      stress        initial stress, in MPa
      times         times to solve for, in hours
  """
  obj = select_obj(material)

  #Below the temperature limit of the ISSCs
  try:
    obj.isochronous(0.01, temperature, times[0])
  except errors.OutofRange:
    return np.array([stress] * len(times))

  srate = lambda s, t: -elastic.youngs(material, temperature, extrapolate = True) * (
      obj.creep(s, temperature, t + dt) - obj.creep(s, temperature, t)) / dt

  return inte.odeint(srate, stress, np.insert(times,0,0))
