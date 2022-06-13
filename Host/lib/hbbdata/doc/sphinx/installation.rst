.. _installation:

Installing hbbdata
==================

General requirements
--------------------

Generally, to property run and validate the package you need to have Python 3.x installed with the following packages:

* `numpy <https://www.numpy.org/>`_
* `scipy <https://www.scipy.org/scipylib/index.html>`_
* `nose <https://pypi.org/project/nose/>`_

All three are very common packages and are available for a variety of operating systems.  The instructions below provide specific instructions on how to install hbbdata on `Ubuntu Linux 18.04 <https://ubuntu.com/>`_, `CentOS 7 <https://www.centos.org/>`_, and Windows 10. 

Ubuntu 18.04 instructions
-------------------------

Download the hbbdata distribution and uncompress it into the directory you want it installed to.  Open a terminal and navigate to the root ``hbbdata/`` directory.

Install the required packages

.. code-block:: console

   sudo apt-get install python3 python3-numpy python3-scipy python3-nose

Run the install validation tests

.. code-block:: console
   
   nosetests3

If successful, the result of the testing should be ``OK``, with the terminal output looking like

.. code-block:: console

   .........................................
   ----------------------------------------------------------------------
   Ran 41 tests in 3.796s

   OK

Add the ``hbbdata/`` root directory to your ``PYTHONPATH`` environment variable, preferably in your ``.bashrc`` file or similar so this step does not need to be repeated each time you open a new terminal.  For example, if the full path to hbbdata is ``/path/to/hbbdata`` and you are using the bash shell, add the following line to your ``.bashrc``

.. code-block:: console
   
   export PYTHONPATH=$PYTHONPATH:/path/to/hbbdata

Now see the :ref:`quickstart` for an example of how to use hbbdata.

CentOS 7 instructions
---------------------

Download the hbbdata distribution and uncompress it into the directory you want it installed to.  Open a terminal and navigate to the root ``hbbdata/`` directory.

Install the IUS set of packages, which contains a python 3 release

.. code-block:: console

   sudo yum install https://centos7.iuscommunity.org/ius-release.rpm 

Install the required packages

.. code-block:: console

   sudo yum install python36 python36-numpy python36-scipy python36-nose

Run the install validation tests

.. code-block:: console
   
   nosetests-3.6

If successful, the result of the testing should be ``OK``, with the terminal output looking like

.. code-block:: console

   .........................................
   ----------------------------------------------------------------------
   Ran 41 tests in 3.796s

   OK

Add the ``hbbdata/`` root directory to your ``PYTHONPATH`` environment variable, preferably in your ``.bashrc`` file or similar so this step does not need to be repeated each time you open a new terminal.  For example, if the full path to hbbdata is ``/path/to/hbbdata`` and you are using the bash shell, add the following line to your ``.bashrc``

.. code-block:: console
   
   export PYTHONPATH=$PYTHONPATH:/path/to/hbbdata

Now see the :ref:`quickstart` for an example of how to use hbbdata.

Windows 10 instructions
-----------------------

These directions assume the use of the Python 3.7 `Anaconda <https://www.anaconda.com/distribution/>`_ distribution to run Python on Windows.  Other methods, including a bare install from the official `Python 3.7 binaries <https://www.python.org/downloads/>`_ are possible, but Anaconda provides the quickest method for installing the dependencies.  These directions assume Anaconda has been installed.

Unzip the hbbdata distribution into the directory you want it installed into.

Open an Anaconda terminal (generally click the Start Menu, then navigate to click on ``Anaconda Prompt``).  Navigate to the hbbdata root directory using the terminal, i.e. 

.. code-block:: console

   cd C:/Users/username/hbbdata

assuming ``C:/Users/username`` is the directory in which you install the package.

Run the install validation tests (all the required packages are already installed in the base Anaconda installation).

.. code-block:: console
   
   nosetests

If successful, the result of the testing should be ``OK``, with the terminal output looking like

.. code-block:: console

   .........................................
   ----------------------------------------------------------------------
   Ran 41 tests in 3.796s

   OK

Use ``conda-develop`` to add hbbdata to your python path.  Identify the full pathname to the directory you installed hbbdata.  Say this path is ``C:/Users/username/hbbdata`` then run the command

.. code-block:: console
   
   conda-develop C:/Users/username/hbbdata

Now see the :ref:`quickstart` for an example of how to use hbbdata.
