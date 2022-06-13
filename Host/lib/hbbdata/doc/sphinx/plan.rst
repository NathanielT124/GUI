.. _plan:

Software quality plan
=====================

Software development plan
-------------------------

This chapter describes the software development quality plan used to create
the hbbdata package.
This particular chapter focuses on development.  Details on 
:ref:`validation` are contained in a separate chapter.

.. _requirements:

Requirements
^^^^^^^^^^^^

The main purpose of this package is to provide an API to access the design
information contained in Section III, Division 5, Subsection HB, Subpart B
of the ASME Boiler & Pressure Vessel Code along with appropriate ancillary information from Section II, Part D and relevant Nuclear Code Cases.

Subpart HBB contains rules for the design of Class A elevated temperature nuclear components.  The Subpart allows the use of a limited selection of materials, listed below.  In addition, a recently passed Nuclear Code Case allows the use of Alloy 617 for Class A construction.  This package includes the Alloy 617 design data, drawn from the current version of the Code Case.  The materials covered by the package are then

* 304SS (304) -- 304H austenitic stainless steel
* 316SS (316) -- 316H austenitic stainless steel
* Ni-Fe-Cr UNS N08810 (800H) -- Alloy 800H Ni-alloy
* 2-1/4Cr-1Mo (2.25Cr-1Mo) -- annealed 2-1/4Cr-1Mo steel
* 9Cr-1Mo-V (gr91) -- modified 9Cr-1Mo, Grade 91 ferritic-martensitic steel
* Alloy 617 (A617) -- 52Ni-22Cr-13Co-9Mo, Alloy 617 (UNS N06617) Ni-alloy

The string keys in parenthesis are important -- these short descriptors are used by the package API to refer to each material.

For a given combination of material and design parameters (almost always temperature and often design life) the package will return the requested material property.  If the combination of requested property, material, and design parameters is invalid, for example the requested temperature is not in the Subpart HBB design range, then the package should return an error.

The Code provides the design data, for the most part, as tables in either Section III, Division 5, Subsection HB, Subpart B, Section II, or the Alloy 617 Code Case.  In general, designers will need the design information at points between the tabulated entries.  The Code does not specify a particular method of interpolation.  The requirement specification here selects a method of interpolation based on engineering judgement, always either linear or log-linear interpolation.  For the tabulated design data the package must correctly read in the Code table defining the property, check the requested design parameters for validity and through an error, if required, and then correctly interpolate the table to the requested value of the parameters.

There are two exceptions to this general requirement.  One is that the isochronous stress-strain curves are provided as figures in the Code, without corresponding tabulated data.  The isochronous curves provide strain as a function of the design parameters of temperature, stress, and time.  To provide arbitrary values of the isochronous stress-strain relation the package implements the original deformation models underlying the isochronous stress-strain curves.  This strategy is outlined in the API reference on the curves.  However, the intent remains the same -- the package must correctly provide values of the curves for arbitrary sets of design parameters.

The second exception are design information based in turn on other design data.  For example, the package must provide minimum time-to-rupture for a given temperature and stress, whereas the Code provides minimum stress-to-rupture for given temperatures and times.  For this case, the required design information is a mathematical rearrangement of other design data and so the package is required to accurately implement the corresponding mathematical formula.

The following sections describe the design data the package must implement.  Each section follows a common format.  It starts with a general overview of the design data, including the units provided by the package.  It then lists the location(s) in the Code providing the information.  Then the section describes the input design parameter and any limits on those design parameters.  Finally, the section lists the method of implementation -- either reading and interpolating from a table (listing the interpolation method) or some mathematical relation to existing design data.

Young's modulus
"""""""""""""""

.. rubric:: Description and units

The elastic Young's modulus of the material in MPa.

.. rubric:: Code reference

Section II, Part D, Tables TM-1 through TM-5.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperature in the corresponding table in Section II, Part D.

.. rubric:: Implementation type

Tabulated values with linear interpolation in temperature.

Poisson's ratio
"""""""""""""""

.. rubric:: Description and units

The elastic Poisson's ratio of the material, unitless.

.. rubric:: Code reference

Section II, Part D, Table PRD.

.. rubric:: Parameters and limits

None, ASME values are constant in temperature.

.. rubric:: Implementation type

Single value.

Thermal expansion coefficient
"""""""""""""""""""""""""""""

.. rubric:: Description and units

The instantaneous thermal expansion coefficient, units of mm/mm/°C.

.. rubric:: Code reference

Section II, Part D, Tables TE-1 through TE-5.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperature in the corresponding table in Section II, Part D.

.. rubric:: Implementation type

Tabulated values with linear interpolation in temperature.

Thermal conductivity
""""""""""""""""""""

.. rubric:: Description and units

Thermal conductivity, units of W/(m °C).

.. rubric:: Code reference

Section II, Part D, Table TCD.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperature in the corresponding table in Section II, Part D.

.. rubric:: Implementation type

Tabulated values with linear interpolation in temperature.

Thermal diffusivity
"""""""""""""""""""

.. rubric:: Description and units

Thermal diffusivity, units of 10\ :sup:`-6` m\ :sup:`2`/s.

.. rubric:: Code reference

Section II, Part D, Table TCD.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperature in the corresponding table in Section II, Part D.

.. rubric:: Implementation type

Tabulated values with linear interpolation in temperature.

Yield strength
""""""""""""""

.. rubric:: Description and units

Code value of yield strength (:math:`S_{y}`), units of MPa.  Optionally reduced for the effect of time and temperature per HBB-2160.

.. rubric:: Code reference

Section II, Part D, Subpart 1, Table Y-1 extended in Section III, Division 5, HBB-I-14.5.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum temperature in Section II, Table Y-1 and the maximum temperature in HBB-I-14.5. 

.. rubric:: Implementation type

Tabulated values with linear interpolation in temperature.

Tensile strength
""""""""""""""""

.. rubric:: Description and units

Code value of tensile strength (:math:`S_{u}`), units of MPa.  Optionally reduced for the effect of time and temperature per HBB-2160.

.. rubric:: Code reference

Section II, Part D, Subpart 1, Table U extended in Section III, Division 5, HBB-3225-1.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum temperature in Section II, Table U and the maximum temperature in HBB-3225-1.

.. rubric:: Implementation type

Tabulated values with linear interpolation in temperature.

Yield strength reduction factor
"""""""""""""""""""""""""""""""

.. rubric:: Description and units

Time-temperature reduction factor for the yield strength, unitless.

.. rubric:: Code reference

Section III, Division 5, Subsection HB, Subpart B Tables HBB-3225-2 and HBB-3225-3A.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperatures in the corresponding HBB tables, and time (hours), limited to be between zero and the maximum design life for the material given by the Subpart HBB allowable stress tables.

.. rubric:: Implementation type

Tabulated values with linear interpolation in temperature and linear interpolation in time or fixed values (depending on the material).

Tensile strength reduction factor
"""""""""""""""""""""""""""""""""

.. rubric:: Description and units

Time-temperature reduction factor for the tensile strength, unitless.

.. rubric:: Code reference

Section III, Division 5, Subsection HB, Subpart B Tables HBB-3225-2, HBB-3225-3B, and HBB-3225-4.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperatures in the corresponding HBB tables, and time (hours), limited to be between zero and the maximum design life for the material given by the Subpart HBB allowable stress tables.

.. rubric:: Implementation type

Tabulated values with linear interpolation in temperature and linear interpolation in time or fixed values (depending on the material).

Allowable stress S\ :sub:`m`
""""""""""""""""""""""""""""

.. rubric:: Description and units

Section III, Division 5 allowable stress :math:`S_{m}`, in MPa, optionally reduced for time-temperature effects per HBB-2160.

.. rubric:: Code reference

HBB-2160(3),(-b) to (-f)

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperatures in the corresponding HBB tables for yield and tensile stress.

.. rubric:: Implementation type

A mathematical relation to the Code values of yield and tensile strength, described in the above-cited section of the Code.

Allowable stress S\ :sub:`t`
""""""""""""""""""""""""""""

.. rubric:: Description and units

Section III, Division 5 allowable stress :math:`S_{t}`, in MPa.

.. rubric:: Code reference

Tables HBB-I-14.4(A to E).

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperatures in the corresponding HBB table, and time (hours), limited to the maximum value given in the corresponding HBB table.

.. rubric:: Implementation type

Tabulated, interpolated linearly in temperature and log-linearly in time.

Allowable stress S\ :sub:`mt`
"""""""""""""""""""""""""""""

.. rubric:: Description and units

Section III, Division 5 allowable stress :math:`S_{mt}`, in MPa.

.. rubric:: Code reference

Defined by HBB-3221 as the lesser of :math:`S_{m}` and :math:`S_{t}`, where :math:`S_{m}` is optionally reduced for time-temperature effects per HBB-2160.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperatures in the corresponding HBB table, and time (hours), limited to the maximum value given in the corresponding HBB table.

.. rubric:: Implementation type

Mathematical relation between :math:`S_{m}` and :math:`S_{t}`.

Allowable stress S\ :sub:`o`
""""""""""""""""""""""""""""

.. rubric:: Description and units

Section III, Division 5 allowable stress :math:`S_{o}`, in MPa.

.. rubric:: Code reference

Table HBB-I-14.2.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperatures in the corresponding HBB table.

.. rubric:: Implementation type

Tabulated, interpolated linearly in temperature.

Time to indicated S\ :sub:`t`
"""""""""""""""""""""""""""""

.. rubric:: Description and units

Given an allowable stress :math:`S_t` and a temperature return the time to that allowable stress.

.. rubric:: Code reference

Tables HBB-I-14.4(A to E).

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperatures in the corresponding HBB table, and stress (MPa), limited to the tabulated values in that table. 

.. rubric:: Implementation type

Mathematical rearrangement of the :math:`S_t` table.

Minimum stress to rupture S\ :sub:`r`
"""""""""""""""""""""""""""""""""""""

.. rubric:: Description and units

Section III, Division 5 minimum stress to rupture :math:`S_{r}`, in MPa.

.. rubric:: Code reference

Table HBB-I-14.6(A to E)

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperatures in the corresponding HBB table, and time (hours), limited to the maximum time in the corresponding HBB table.

.. rubric:: Implementation type

Tabulated, interpolated linearly in temperature and log-linearly in time.

Time to indicated S\ :sub:`r`
"""""""""""""""""""""""""""""

.. rubric:: Description and units

Given an allowable stress :math:`S_r` and a temperature return the time in hours to that rupture stress.

.. rubric:: Code reference

Table HBB-I-14.6(A to E)

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperatures in the corresponding HBB table, and stress (MPa), limited to the tabulated values in that table. 

.. rubric:: Implementation type

Mathematical rearrangement of the :math:`S_r` table.

Strain range to allowable design cycles :math:`\varepsilon_t`
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. rubric:: Description and units

Strain range (mm/mm) giving the provided cycles to failure.

.. rubric:: Code reference

Figures HBB-T-1410-1(A to E)

.. rubric:: Parameters and limits

Temperature (°C), limited to the maximum temperature for which there is a fatigue curve in HBB-T-1410, and number of design cycles, limited to the maximum values in HBB-T-1410.

.. rubric:: Implementation type

Tabulated.  Bounding in temperature -- use fatigue curve closest, but greater, than the provided temperature.  Interpolate log-linearly in cycles.

Allowable design cycles :math:`N_d`
"""""""""""""""""""""""""""""""""""

.. rubric:: Description and units

Design allowable fatigue cycles.

.. rubric:: Code reference

Figures HBB-T-1410-1(A to E)

.. rubric:: Parameters and limits

Temperature (°C), limited to the maximum temperature for which there is a fatigue curve in HBB-T-1410, and the strain range (mm/mm).

.. rubric:: Implementation type

Mathematical rearrangement of the design fatigue curves.

Creep-fatigue interaction diagram
"""""""""""""""""""""""""""""""""

.. rubric:: Description and units

Report whether the provided fatigue damage (:math:`D_f`) and creep damage (:math:`D_c`) falls within the Code design creep-fatigue interaction diagram.

.. rubric:: Code reference

Figure HBB-T-1410-2.

.. rubric:: Parameters and limits

Unitless input creep and fatigue damage fractions.

.. rubric:: Implementation type

Fully described by Figure HBB-T-1410-2.

Isochronous stress-strain curve values
""""""""""""""""""""""""""""""""""""""

.. rubric:: Description and units

Strains (mm/mm) corresponding to the provided design parameters describing the total deformation accumulated by the material under those conditions.

.. rubric:: Code reference

Figures in HBB-T-1800.

.. rubric:: Parameters and limits

Temperature (°C), limited to the maximum and minimum temperatures for which HBB-T-1800 provides a design curve.  Stress, in MPa.  Time, in hours, limited to the maximum time curve provided in HBB-T-1800. 

.. rubric:: Implementation type

Unique among all the design data provided by the package.  The Code provides the plotted isochronous curves in HBB-T-1800.  However, it is very difficult to provide arbitrary values of strain based on these figures.  Instead, the package should implement the deformation models underlying the Code isochronous curves directly.  These equations generally match the Code plots.  Small discrepancies will be corrected by future Code action.

Hot tensile curve values
""""""""""""""""""""""""

.. rubric:: Description and units

Strains (mm/mm) corresponding to the provided design parameters describing the time-independent deformation accumulated by the material under those conditions.

.. rubric:: Code reference

Figures HBB-T-1800.

.. rubric:: Parameters and limits

Temperature (°C), limited to the maximum temperature for which there is a design curve given in HBB-T-1800.

.. rubric:: Implementation type

The zero-time isochronous stress-strain curve.

Pseudo yield stress for Code Case N-861
"""""""""""""""""""""""""""""""""""""""

.. rubric:: Description and units

Pseudoyield stress (in MPa) for Code Case N-861 (EPP strain limits code case).  Defined as the minimum of the Code yield strength at the provided temperature and the inelastic strain implied by the isochronous stress-strain curve for the given temperature, target strain, and time.

.. rubric:: Code reference

Code Case N-861.

.. rubric:: Parameters and limits

Temperature (°C), limited to the minimum and maximum temperature for which Section III, Division 5 provides an ischronous stress-strain curve.  Design life (hours), limited to the maximum time for which Section III, Division 5 provides an isochronous curve.  Target strain (mm/mm), limited to be less than 2%.

.. rubric:: Implementation type

Mathematical rearrangement of the isochronous stress-strain curve values and 
Code yield strength.

Pseudo yield stress for Code Case N-862
"""""""""""""""""""""""""""""""""""""""

.. rubric:: Description and units

Pseudoyield stress (in MPa) for Code Case N-862 (EPP creep-fatigue code case).  Defined as the minimum of the Code yield strength at the provided temperature and the Code minimum stress to rupture at the given temperature and time.

.. rubric:: Code reference

Code Case N-861.

.. rubric:: Parameters and limits

Temperature (°C) and time (hours), limited to the values for which there is a minimum stress to rupture (:math:`S_r`) in Section III, Division 5.

.. rubric:: Implementation type

Mathematical rearrangement of the minimum stress to rupture values and 
Code yield strength.

Configuration management
^^^^^^^^^^^^^^^^^^^^^^^^

Package software development is managed on the internal Argonne National Laboratory GitLab system.  This development system combines version control through a git repository, a ticketing system for requesting and documenting software development and changes, and access control to enforce quality control procedures.

Each feature, fulfilling one of the requirements above, will be developed on a separate branch in the git repository.  Once the new branch completely implements the required feature it will be merged into the main code using a gitlab pull request.  To accept the full request the following process should be followed:

1. Developers may not accept their own pull request.  Instead a separate peer-review should be completed by another developer.  This peer review should ensure 1) the pull request meets all the requirements listed here and 2) the code contained in the pull request is off good general quality, is clear, and well-documented with comments in the code.
2. In addition to the code, a pull request must provide a test suite fulfilling the requirements in :ref:`validation`.  The composite test suite, once all the software features have been implemented, will serve as the final verification and validation method for the project.
3. The branch must pass the project python style requirements, as checked by the pylint tool.

Gitlab automatically enforces all three requirements -- it will not allow a pull request to be merged unless it has undergone peer review, automatically passes all the tests, and meets the pylint style requirements.  The peer-reviewer is responsible for ensuring the code is clear and documented with comments and that the developer has added sufficient tests to verify and validate the new features.

Software risk management
------------------------

The primary risk is that the package will return inaccurate or invalid design data to a user request.  The :ref`validation` plan is the primary method for mitigating this risk.

A secondary risk is a change to the end user's system configuration preventing the package from installing or running correctly.  This risk is mitigated by writing the package in a cross-platform, interpreted language (Python) and providing installation checks to verify that the package is correctly installed on a new system. 
