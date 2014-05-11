SmartList
=========

A collection of data structures that are backed by an actual list.
The backing elements can be transformed or filtered.
Updates to the backing list also update the smart list.
Updates to the smart list propogate back to the backing list

How to Use
----------

When you construct the smart list, pass it the original list and optionally a
transform function, untransform function, and a filter function to be run on each element.
You can also subclass the smartlist class to provide more advanced callback functions.

[![Build Status](https://travis-ci.org/hufman/SmartList.svg?branch=master)](https://travis-ci.org/hufman/SmartList)
