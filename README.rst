Summary
=======

Nose plugin that makes xunit xml reports work when running tests on
more than one cpu.

Installation
============

::

  $ pip install nose_xunitmp


Usage
=====

::

  $ nosetests --with-xunitmp
  $ nosetests --xunitmp-file results.xml
