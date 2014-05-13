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

The SmartListFromList class is pretty simple. The transform function accepts a single list item and must return another list item. The untransform function accepts a list item and must return a single list item to add to the backing list. The filter function accepts a backing list item and must return a boolean of whether to include the backing list item.

The SmartDictFromList class is slightly different. The transform function accepts a single list item and must return a 2-tuple of (key, value). The untransform function accepts a key and value parameter and must return a single item to add to the backing list. The filter function accepts a backing list item and must return a boolean of whether to include the backing list item.

The MultiListFromList is extra special. The transform function accepts a single list item and must return a list. The untransform function accepts a list, which may be empty, and must return a list item, or None to have the item removed from the backing list. The filter function accepts a backing item and must return a boolean of whether to include the backing list item.

[![Build Status](https://travis-ci.org/hufman/SmartList.svg?branch=master)](https://travis-ci.org/hufman/SmartList)
