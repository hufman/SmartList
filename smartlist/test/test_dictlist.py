import sys
import unittest
import smartlist


class TestDictList(unittest.TestCase):
	def test_serialize(self):
		baselist = ['1=a', '2=b', '3=t']
		mydict = smartlist.SmartDictFromList(
		    baselist,
		    transform=lambda x: (int(x.split('=', 1)[0]), x.split('=', 1)[1]),
		    untransform=lambda k, v: "%s=%s" % (k, v)
		)
		keys = [1, 2, 3]
		values = ["a", "b", "t"]
		items = list(zip(keys, values))
		if sys.version_info[0] == 2:
			self.assertEqual(keys, mydict.keys())
			self.assertEqual(values, mydict.values())
			self.assertEqual(items, mydict.items())
			iterkeys = mydict.iterkeys()
			itervalues = mydict.itervalues()
			iteritems = mydict.iteritems()
		else:
			iterkeys = mydict.keys()
			itervalues = mydict.values()
			iteritems = mydict.items()
		# check main dict for contains
		for key in keys:
			self.assertTrue(key in mydict)
		# check item views for contains
		for key in keys:
			self.assertTrue(key in iterkeys)
		for value in values:
			self.assertTrue(value in itervalues)
		for item in items:
			self.assertTrue(item in iteritems)
		# check that the iterators are correct
		self.assertEquals(keys, list(mydict.keys()))
		self.assertEquals(values, list(mydict.values()))
		self.assertEquals(items, list(mydict.items()))

	def test_modification_orig(self):
		baselist = ['1=a', '2=b', '3=t']
		mydict = smartlist.SmartDictFromList(
		    baselist,
		    transform=lambda x: (int(x.split('=', 1)[0]), x.split('=', 1)[1]),
		    untransform=lambda k, v: "%s=%s" % (k, v)
		)
		baselist[1] = '4=s'
		baselist.append('5=z')
		keys = [1, 4, 3, 5]
		values = ["a", "s", "t", "z"]
		items = list(zip(keys, values))
		self.assertEquals(keys, list(mydict.keys()))
		self.assertEquals(values, list(mydict.values()))
		self.assertEquals(items, list(mydict.items()))
		del baselist[2]
		keys = [1, 4, 5]
		values = ["a", "s", "z"]
		items = list(zip(keys, values))
		self.assertEquals(keys, list(mydict.keys()))
		self.assertEquals(values, list(mydict.values()))
		self.assertEquals(items, list(mydict.items()))
		baselist.extend(["8=e", "9=f"])
		keys = [1, 4, 5, 8, 9]
		values = ["a", "s", "z", "e", "f"]
		items = list(zip(keys, values))
		self.assertEquals(keys, list(mydict.keys()))
		self.assertEquals(values, list(mydict.values()))
		self.assertEquals(items, list(mydict.items()))

	def test_modification_other(self):
		baselist = ['1=a', '2=b', '3=t']
		mydict = smartlist.SmartDictFromList(
		    baselist,
		    transform=lambda x: (int(x.split('=', 1)[0]), x.split('=', 1)[1]),
		    untransform=lambda k, v: "%s=%s" % (k, v)
		)
		mydict['4'] = 's'
		self.assertEquals(['1=a', '2=b', '3=t', '4=s'], baselist)
		del mydict[2]
		self.assertEquals(['1=a', '3=t', '4=s'], baselist)
		mydict.update({3: "z", 6: "r"})
		self.assertEquals(['1=a', '3=z', '4=s', '6=r'], baselist)

	def test_filtered(self):
		baselist = ['1=a', '2=b', '3=t']
		mydict = smartlist.SmartDictFromList(
		    baselist,
		    transform=lambda x: (int(x.split('=', 1)[0]), x.split('=', 1)[1]),
		    untransform=lambda k, v: "%s=%s" % (k, v),
		    filter=lambda x: int(x.split('=', 1)[0]) % 2 == 0
		)
		keys = [2]
		values = ["b"]
		items = list(zip(keys, values))
		self.assertEquals(keys, list(mydict.keys()))
		self.assertEquals(values, list(mydict.values()))
		self.assertEquals(items, list(mydict.items()))
		baselist.append('4=s')
		keys = [2, 4]
		values = ["b", "s"]
		items = list(zip(keys, values))
		self.assertEquals(keys, list(mydict.keys()))
		self.assertEquals(values, list(mydict.values()))
		self.assertEquals(items, list(mydict.items()))
