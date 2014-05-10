class SmartListFromList(object):
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
		return elem

	def untransform(self, elem):
		return elem

	def filter(self, elem):
		return True

	def untransformed_index_of(self, elem):
		for index in range(0, len(self.list)):
			if self.filter(self.list[index]) and \
			   self.transform(self.list[index]) == elem:
				return index
		return ValueError("%s is not in list"%(elem,))

	def untransformed_index(self, index):
		if index >= 0:
			counted = -1
			for i in range(0, len(self.list)):
				if self.filter(self.list[i]):
					counted = counted + 1
				if counted == index:
					return i
		else:
			counted = 0
			for i in range(len(self.list)-1, -1, -1):
				if self.filter(self.list[i]):
					counted = counted - 1
				if counted == index:
					return i
		return IndexError("list index out of range")

	# list magic methods
	def __len__(self):
		counted = 0
		for index in range(0, len(self.list)):
			if self.filter(self.list[index]):
				counted = counted + 1
		return counted

	def __getitem__(self, index):
		untransformed_index = self.untransformed_index(index)
		return self.transform(self.list[untransformed_index])

	def __setitem__(self, index, elem):
		untransformed_index = self.untransformed_index(index)
		self.list[untransformed_index] = self.untransform(elem)

	def __delitem__(self, index):
		untransformed_index = self.untransformed_index(index)
		del self.list[untransformed_index]

	def __iter__(self):
		return (self.transform(elem) for elem in self.list if self.filter(elem))

	def __contains__(self, elem):
		for e in self.list:
			if self.filter(e) and \
			   self.transform(e) == elem:
				return True
		return False

	# list functionality
	def append(self, elem):
		self.list.append(self.untransform(elem))

	def extend(self, otherlist):
		for elem in otherlist:
			self.list.append(self.untransform(elem))

	def insert_before(self, index, elem):
		untransformed_index = self.untransformed_index(index)
		self.list.insert(untransformed_index, self.untransform(elem))

	def insert_after(self, index, elem):
		untransformed_index = self.untransformed_index(index)
		self.list.insert(untransformed_index + 1, self.untransform(elem))

	insert = insert_before

	def remove(self, elem):
		self.list.remove(self.untransform(elem))

	def pop(self, index=-1):
		untransformed_index = self.untransformed_index(index)
		return self.transform(self.list.pop(untransformed_index))
		if index < 0:
			raise IndexError("pop index out of range")

	def index(self, elem):
		counted = -1
		for index in range(0, len(self.list)):
			if self.filter(self.list[index]):
				counted = counted + 1
			if self.transform(self.list[index]) == elem:
				return counted
		return ValueError("%s is not in list"%(elem,))

	def count(self, elem):
		counted = 0
		for index in range(0, len(self.list)):
			if self.filter(self.list[index]) and \
			   self.transform(self.list[index]) == elem:
				counted = counted + 1
		return counted

	def sort(self):
		indices = []
		for index in range(0, len(self.list)):
			if self.filter(self.list[index]):
				indices.append(index)
		sorted_indices = sorted(indices, key=lambda i: self.transform(self.list[i]))
		sorted_items = [self.list[i] for i in sorted_indices]
		for index in range(0, len(indices)):
			self.list[indices[index]] = sorted_items[index]

	def reverse(self):
		indices = []
		for index in range(0, len(self.list)):
			if self.filter(self.list[index]):
				indices.append(index)
		for l,r in zip(indices, reversed(indices)):
			if l >= r:
				break
			c = self.list[l]
			self.list[l] = self.list[r]
			self.list[r] = c
