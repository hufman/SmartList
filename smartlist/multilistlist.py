import sys
PY2 = sys.version_info[0] == 2
if PY2:
	irange = xrange
else:
	irange = range


class MultiListFromList(object):
	def __init__(self, list, transform=None, untransform=None, filter=None):
		self.list = list
		if transform:
			self.transform = transform
		if untransform:
			self.untransform = untransform
		if filter:
			self.filter = filter

	# smart functionality
	def transform(self, elem):
		return [elem]

	def untransform(self, elem):
		return elem[0]

	def filter(self, elem):
		return True

	def untransformed_index_of(self, elem):
		for index in irange(0, len(self.list)):
			if self.filter(self.list[index]):
				for obj in self.transform(self.list[index]):
					if obj == elem:
						return index
		raise ValueError("%s is not in list" % (elem,))

	def untransformed_index_of_ex(self, elem):
		for index in irange(0, len(self.list)):
			mainobj = self.list[index]
			if self.filter(mainobj):
				subobj = self.transform(mainobj)
				for subindex in irange(0, len(subobj)):
					if subobj[subindex] == elem:
						return index, subindex
		raise ValueError("%s is not in list" % (elem,))

	def untransformed_index_ex(self, index):
		if index >= 0:
			counted = -1
			for i in irange(0, len(self.list)):
				mainobj = self.list[i]
				if self.filter(mainobj):
					for j in irange(0, len(self.transform(mainobj))):
						counted = counted + 1
						if counted == index:
							return i, j
		else:
			counted = 0
			for i in irange(len(self.list) - 1, -1, -1):
				mainobj = self.list[i]
				if self.filter(mainobj):
					for j in irange(len(self.transform(mainobj)) -1, -1, -1):
						counted = counted - 1
						if counted == index:
							return i, j
		raise IndexError("list index out of range")

	def untransformed_index(self, index):
		return self.untransformed_index_ex(index)[0]

	# list magic methods
	def __len__(self):
		counted = 0
		for index in irange(0, len(self.list)):
			if self.filter(self.list[index]):
				counted = counted + len(self.transform(self.list[index]))
		return counted

	def __getitem__(self, index):
		if isinstance(index, slice):
			return list(self)[index]
		else:
			untransformed_index, subindex = self.untransformed_index_ex(index)
			obj = self.transform(self.list[untransformed_index])
			return obj[subindex]

	def __setitem__(self, index, elem):
		untransformed_index, subindex = self.untransformed_index_ex(index)
		obj = self.transform(self.list[untransformed_index])
		obj[subindex] = elem
		self.list[untransformed_index] = self.untransform(obj)

	def __delitem__(self, index):
		untransformed_index, subindex = self.untransformed_index_ex(index)
		obj = self.transform(self.list[untransformed_index])
		del obj[subindex]
		newobj = self.untransform(obj)
		if newobj is not None:
			self.list[untransformed_index] = newobj
		else:
			del self.list[untransformed_index]

	def __iter__(self):
		for elem in self.list:
			if self.filter(elem):
				for subobj in self.transform(elem):
					yield subobj

	def __contains__(self, elem):
		for obj in self.list:
			if self.filter(obj):
				for subobj in self.transform(obj):
					if subobj == elem:
						return True
		return False

	# list functionality
	def append(self, elem):
		try:
			untransformed_index, subindex = self.untransformed_index_ex(-1)
			obj = self.transform(self.list[untransformed_index])
			obj.append(elem)
			self.list[untransformed_index] = self.untransform(obj)
		except IndexError:
			obj = [elem]
			self.list.append(self.untransform(elem))

	def extend(self, otherlist):
		try:
			untransformed_index, subindex = self.untransformed_index_ex(-1)
			obj = self.transform(self.list[untransformed_index])
			obj.extend(otherlist)
			self.list[untransformed_index] = self.untransform(obj)
		except IndexError:
			obj = otherlist
			self.list.append(self.untransform(obj))

	def insert(self, index, elem):
		untransformed_index, subindex = self.untransformed_index_ex(index)
		obj = self.transform(self.list[untransformed_index])
		obj.insert(subindex, elem)
		self.list[untransformed_index] = self.untransform(obj)

	def remove(self, elem):
		untransformed_index, subindex = self.untransformed_index_of_ex(elem)
		obj = self.transform(self.list[untransformed_index])
		del obj[subindex]
		newobj = self.untransform(obj)
		if newobj is not None:
			self.list[untransformed_index] = newobj
		else:
			del self.list[untransformed_index]

	def pop(self, index=-1):
		untransformed_index, subindex = self.untransformed_index_ex(index)
		subobj = self.transform(self.list[untransformed_index])
		print("index: %s   Subindex: %s"%(index, subindex,))
		ret = subobj.pop(subindex)
		newobj = self.untransform(subobj)
		if newobj is not None:
			self.list[untransformed_index] = newobj
		else:
			del self.list[untransformed_index]
		return ret

	def index(self, elem):
		counted = -1
		for index in irange(0, len(self.list)):
			if self.filter(self.list[index]):
				for obj in self.transform(self.list[index]):
					counted = counted + 1
					if obj == elem:
						return counted
		return ValueError("%s is not in list" % (elem,))

	def count(self, elem):
		counted = 0
		for index in irange(0, len(self.list)):
			if self.filter(self.list[index]):
				for obj in self.transform(self.list[index]):
					if obj == elem:
						counted = counted + 1
		return counted

	def sort(self):
		subobjects = sorted(list(self))
		for index in irange(0, len(self.list)):
			if self.filter(self.list[index]):
				obj = self.transform(self.list[index])
				newobj = self.untransform(subobjects[:len(obj)])
				del subobjects[:len(obj)]
				self.list[index] = newobj

	def reverse(self):
		subobjects = list(self)
		subobjects.reverse()
		for index in irange(0, len(self.list)):
			if self.filter(self.list[index]):
				obj = self.transform(self.list[index])
				newobj = self.untransform(subobjects[:len(obj)])
				del subobjects[:len(obj)]
				self.list[index] = newobj
