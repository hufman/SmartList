import unittest
import smartlist


class TestMultiListList(unittest.TestCase):
	def test_serialize(self):
		baselist = ["1,2", "3,4"]
		mylist = smartlist.MultiListFromList(
		    baselist,
		    transform=lambda x: [int(i) for i in x.split(',')],
		    untransform=lambda x: ','.join([str(i) for i in x]) if len(x)>0 else None
		)
		self.assertEqual([1, 2, 3, 4], list(mylist))
		self.assertEqual(1, mylist.count(2))
		self.assertEqual(2, mylist.index(3))
		self.assertTrue(2 in mylist)
		reallist = [1, 2, 3, 4]
		for item in mylist:
			self.assertEqual(reallist.pop(0), item)

	def test_modification_orig(self):
		baselist = ["1,2", "3,4"]
		mylist = smartlist.MultiListFromList(
		    baselist,
		    transform=lambda x: [int(i) for i in x.split(',')],
		    untransform=lambda x: ','.join([str(i) for i in x]) if len(x)>0 else None
		)
		self.assertEqual([1, 2, 3, 4], list(mylist))
		baselist[0] = "1,5"
		baselist.append("6")
		self.assertEqual([1, 5, 3, 4, 6], list(mylist))
		del baselist[1]
		self.assertEqual([1, 5, 6], list(mylist))
		baselist.extend(["7", "8"])
		self.assertEqual([1, 5, 6, 7, 8], list(mylist))

	def test_modification_other(self):
		baselist = ["1,2", "3"]
		mylist = smartlist.MultiListFromList(
		    baselist,
		    transform=lambda x: [int(i) for i in x.split(',')],
		    untransform=lambda x: ','.join([str(i) for i in x]) if len(x)>0 else None
		)
		self.assertEqual(2, len(baselist))
		self.assertEqual(3, len(mylist))
		mylist[1] = 5
		mylist.append(4)
		self.assertEqual(["1,5", "3,4"], baselist)
		del mylist[2]
		self.assertEqual(["1,5", "4"], baselist)
		mylist.extend([7, 8])
		self.assertEqual(["1,5", "4,7,8"], baselist)
		self.assertEqual(8, mylist.pop())
		self.assertEqual(["1,5", "4,7"], baselist)
		self.assertEqual(4, mylist.pop(2))
		self.assertEqual(["1,5", "7"], baselist)

	def test_filtered(self):
		baselist = ["1,2", 3]
		subdata = smartlist.MultiListFromList(
		    baselist,
		    transform=lambda x: [int(i) for i in x.split(',')],
		    untransform=lambda x: ','.join([str(i) for i in x]) if len(x)>0 else None,
		    filter=lambda x: isinstance(x, str)
		)
		self.assertEqual([1, 2], list(subdata))
		baselist.append("-1")
		self.assertEqual([1, 2, -1], list(subdata))
		subdata.sort()
		self.assertEqual([-1, 1, 2], list(subdata))
		self.assertEqual(["-1,1", 3, "2"], baselist)
		subdata.reverse()
		self.assertEqual([2, 1, -1], list(subdata))
		self.assertEqual(["2,1", 3, "-1"], baselist)
		self.assertEqual(-1, subdata.pop())
		self.assertEqual([2, 1], list(subdata))
		self.assertEqual(["2,1", 3], baselist)
		subdata.remove(1)
		self.assertEqual([2], list(subdata))
		self.assertEqual(["2", 3], baselist)
