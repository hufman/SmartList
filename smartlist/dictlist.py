import sys
PY2 = sys.version_info.major == 2


class SmartDictFromList(object):
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

	def untransformed_index_of(self, key):
		for index in range(0, len(self.list)):
			if self.filter(self.list[index]) and \
			   self.transform(self.list[index])[0] == key:
				return index
		raise KeyError(index)

	# dict magic methods
	def __len__(self):
		counted = 0
		for elem in self.list:
			if self.filter(elem):
				counted = counted + 1
		return counted

	def __getitem__(self, key):
		untransformed_index = self.untransformed_index_of(key)
		return self.transform(self.list[untransformed_index])

	def __setitem__(self, key, value):
		try:
			untransformed_index = self.untransformed_index_of(key)
			self.list[untransformed_index] = self.untransform(key, value)
		except KeyError:
			self.list.append(self.untransform(key, value))

	def __delitem__(self, key):
		untransformed_index = self.untransformed_index_of(key)
		del self.list[untransformed_index]

	def __iter__(self):
		return (self.transform(elem) for elem in self.list if self.filter(elem))

	def __contains__(self, key):
		for elem in self.list:
			if self.filter(elem) and \
			   self.transform(elem)[0] == key:
				return True
		return False

	# dict functionality
	def clear(self):
		for index in range(len(self.list) + 1, -1, -1):
			if self.filter(self.list[index]):
				del self.list[index]

	def copy(self):
		ret = {}
		for index in range(0, len(self.list)):
			if self.filter(elem):
				item = self.transform(elem)
				ret[item[0]] = item[1]
		return ret

	@classmethod
	def fromkeys(seq, value=None):
		return dict.fromkeys(seq, value)

	def get(self, key, default=None):
		for elem in self.list:
			if self.filter(elem):
				transformed = self.transform(elem)
				if transformed[0] == key:
					return transformed[1]
		return default

	has_key = __contains__

	if PY2:
		def items(self):
			items = []
			for elem in self.list:
				if self.filter(elem):
					transformed = self.transform(elem)
					items.append(transformed)
			return items

		def keys(self):
			keys = []
			for elem in self.list:
				if self.filter(elem):
					transformed = self.transform(elem)
					keys.append(transformed[0])
			return keys

		def values(self):
			values = []
			for elem in self.list:
				if self.filter(elem):
					transformed = self.transform(elem)
					values.append(transformed[1])
			return values

		def iteritems(self):
			for elem in self.list:
				if self.filter(elem):
					transformed = self.transform(elem)
					yield transformed

		def iterkeys(self):
			for elem in self.list:
				if self.filter(elem):
					transformed = self.transform(elem)
					yield transformed[0]

		def itervalues(self):
			for elem in self.list:
				if self.filter(elem):
					transformed = self.transform(elem)
					yield transformed[1]

		iter = iterkeys

	else:
		def items(self):
			return DictView(self, lambda x: x)

		def keys(self):
			return DictView(self, lambda x: x[0])

		def values(self):
			return DictView(self, lambda x: x[1])

		def iter(self):
			return iter(DictView(self, lambda x: x[0]))

	def remove(self, elem):
		self.list.remove(self.untransform(elem))

	def pop(self, key, default=None):
		try:
			untransformed_index = self.untransformed_index_of(key)
		except KeyError as e:
			if default is None:
				raise
			else:
				return default
		return self.transform(self.list.pop(untransformed_index))[1]

	def popitem(self):
		for index in range(0, len(self.list)):
			if self.filter(self.list[index]):
				transformed = self.transform(self.list[index])
				del self.filter[index]
				return transformed
		raise KeyError("dictionary is empty")

	def setdefault(self, key, default=None):
		try:
			value = self[key]
		except KeyError:
			self[key] = default
			return default

	def update(self, otherdict):
		# get the list of what keys are in the list
		keylocations = {}
		for index in range(0, len(self.list)):
			if self.filter(self.list[index]):
				item = self.transform(self.list[index])
				keylocations[item[0]] = index

		# add the otherdict
		if PY2:
			items = otherdict.iteritems()
		else:
			items = otherdict.items()
		for key, value in items:
			if key in keylocations:
				self.list[keylocations[key]] = self.untransform(key, value)
			else:
				self.list.append(self.untransform(key, value))


class DictView(object):
	def __init__(self, parent, sectioner):
		self.parent = parent
		self.sectioner = sectioner

	def len(self):
		return len(self.parent)

	def iter(self):
		for elem in self.parent.list:
			if self.parent.filter(elem):
				item = self.parent.transform(elem)
				yield self.sectioner(item)

	__iter__ = iter

	def __contains__(self, value):
		for elem in self.parent.list:
			if self.parent.filter(elem):
				item = self.parent.transform(elem)
				item = self.sectioner(item)
				if item == value:
					return True
		return False
