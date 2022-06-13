.. _quickstart:

Quickstart guide
================

This guide assumes you have followed the installation instructions and have added hbbdata to your ``PYTHONPATH``.

Open up a terminal and run Python 3.7.  First test to make sure you can import the hbbdata module::
   
   >>> import hbbdata

If this command runs without error keep going.  If not go back to :ref:`installation`.  

The hbbdata API is divided into a number of modules, each containing logically similar functions accessing the Division 5 design data.  For more details see :ref:`api`.

As an example, let's find the ASME Section II Young's modulus of 316SS at 700°C.  Simply type::

   >>> from hbbdata import elastic
   >>> elastic.youngs("316", 700)
   140000.0

Or we could look up the design yield strength of Alloy 800H at 550°C::

   >>> from hbbdata import plastic
   >>> plastic.yield_stress("800H", 550)
   108.0

A slightly more complicated example might be to determine if the point represented by a fatigue damage fraction of 0.1 and a creep damage fraction of 0.4 falls within the design creep-fatigue interaction diagram from 2-1/4Cr-1Mo steel::

   >>> from hbbdata import interaction
   >>> interaction.inside_envelope("2.25Cr-1Mo", 0.1, 0.4)
   False

As a final example, find the strain corresponding to a stress of 120 MPa for the 9Cr-1Mo-V isochronous stress-strain curve for 525°C and 120,000 hours design life::

   >>> from hbbdata import isochronous
   >>> isochronous.strain_to_time_stress("gr91", 525, 120000.0, 220)
   0.05559105838726914

All of the design data can be accessed through these and similar functions, which are fully described in the :ref:`api`.
