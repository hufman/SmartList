import unittest
import smartlist

class TestListList(unittest.TestCase):
	def test_serialize(self):
		baselist = [1, 2, 3]
		mylist = smartlist.list(baselist, 
		    transform=lambda x:str(x),
		    untransform=lambda x:int(x)
		)
		self.assertEqual(["1","2","3"], list(mylist))
		self.assertEqual(1, mylist.count("2"))
		self.assertEqual(2, mylist.index("3"))
		self.assertTrue("2" in mylist)
		reallist = list(mylist)
		for item in mylist:
			self.assertEqual(reallist.pop(0), item)

	def test_modification_orig(self):
		baselist = [1, 2, 3]
		mylist = smartlist.list(baselist, 
		    transform=lambda x:str(x),
		    untransform=lambda x:int(x)
		)
		self.assertEqual(3, len(mylist))
		baselist[1] = 5
		baselist.append(4)
		self.assertEqual(["1","5","3","4"], list(mylist))
		del baselist[2]
		self.assertEqual(["1","5","4"], list(mylist))
		baselist.extend([7,8])
		self.assertEqual(["1","5","4","7","8"], list(mylist))

	def test_modification_other(self):
		baselist = [1, 2, 3]
		mylist = smartlist.list(baselist, 
		    transform=lambda x:str(x),
		    untransform=lambda x:int(x)
		)
		self.assertEqual(3, len(baselist))
		self.assertEqual(3, len(mylist))
		mylist[1] = '5'
		mylist.append('4')
		self.assertEqual([1,5,3,4], baselist)
		del mylist[2]
		self.assertEqual([1,5,4], baselist)
		mylist.extend(['7','8'])
		self.assertEqual([1,5,4,7,8], baselist)
		self.assertEqual('8', mylist.pop())
		self.assertEqual([1,5,4,7], baselist)
		self.assertEqual('4', mylist.pop(2))
		self.assertEqual([1,5,7], baselist)

	def test_filtered(self):
		baselist = [1, 2, 3]
		evenlist = smartlist.list(baselist, 
		    transform=lambda x:str(x),
		    untransform=lambda x:int(x),
		    filter=lambda x:x%2==0
		)
		self.assertEqual(["2"], list(evenlist))
		baselist.append(4)
		self.assertEqual(["2","4"], list(evenlist))
		evenlist.insert_before(0, "0")
		self.assertEqual(["0","2","4"], list(evenlist))
		self.assertEqual([1,0,2,3,4], baselist)
		evenlist.insert_after(0, "8")
		self.assertEqual(["0","8","2","4"], list(evenlist))
		self.assertEqual([1,0,8,2,3,4], baselist)
		evenlist.sort()
		self.assertEqual(["0","2","4","8"], list(evenlist))
		self.assertEqual([1,0,2,4,3,8], baselist)
		evenlist.reverse()
		self.assertEqual(["8","4","2","0"], list(evenlist))
		self.assertEqual([1,8,4,2,3,0], baselist)
		self.assertEqual("0", evenlist.pop())
		self.assertEqual(["8","4","2"], list(evenlist))
		self.assertEqual([1,8,4,2,3], baselist)
		self.assertEqual("4", evenlist.pop(1))
		self.assertEqual(["8","2"], list(evenlist))
		self.assertEqual([1,8,2,3], baselist)
		evenlist.remove("8")
		self.assertEqual(["2"], list(evenlist))
		self.assertEqual([1,2,3], baselist)
