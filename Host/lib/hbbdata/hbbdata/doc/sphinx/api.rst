.. _api:

API description and documentation
=================================

General overview
----------------

This section describes the complete public API of the hbbdata package.  In general, functions providing Section III, Division 5 design data will take as parameters a material, a temperature, other design parameters, and optional parameters describing options in the Code that are not always taken.

The convention for relating each Class A material to a string key, used in identifying the material in the package, is given in the following table:

.. list-table:: Material keys
   :widths: 25 25
   :header-rows: 1

   * - Material
     - Key
   * - 304SS
     - 304
   * - 316SS
     - 316
   * - Ni-Fe-Cr UNS N08810
     - 800H
   * - 2-1/4Cr-1Mo
     - 2.25Cr-1Mo
   * - 9Cr-1Mo-V
     - gr91
   * - Alloy 617
     - A617

In all cases package unites are consistent with the following unit system:

.. list-table:: Unit system
   :widths: 30 15
   :header-rows: 1
   
   * - Type
     - Units
   * - Stress
     - MPa
   * - Temperature
     - °C
   * - Time
     - hours
   * - Strain
     - mm/mm

API documentation
-----------------

The hbbdata package is divided into a number of submodules, each containing logically related sets of design data functions.  The following sections document each module individually.

In addition to this public API, the package also contains a number of helper functions designed to read and interpolate data and aid in testing.  These functions are documented with Python docstrings in their individual source files.

elastic
"""""""
.. automodule:: hbbdata.elastic
   :members:

thermal
"""""""
.. automodule:: hbbdata.thermal
   :members:

plastic
"""""""
.. automodule:: hbbdata.plastic
   :members:

intensities
"""""""""""
.. automodule:: hbbdata.intensities
   :members:

rupture
"""""""
.. automodule:: hbbdata.rupture
   :members:

fatigue
"""""""
.. automodule:: hbbdata.fatigue
   :members:

interaction
"""""""""""
.. automodule:: hbbdata.interaction
   :members: distance_envelope, inside_envelope, interaction_fatigue, interaction_creep

isochronous
"""""""""""
.. automodule:: hbbdata.isochronous
   :members: isochronous, hot_tensile, strain_to_time_stress, issc_relaxation_analysis_stress, issc_relaxation_analysis_strain

epp
"""
.. automodule:: hbbdata.epp
   :members:

limits
""""""

.. automodule:: hbbdata.limits
   :members:
