import utils as util

# dataBin class manages and preprocesses all of our data
class dataBin:
	# constructor takes a single object, which will contain the data, reverseLookup information, continuous and discrete bins, attributes, and the name of our relation
	def __init__(self, data):
		self.data = data['data'] 				# our primary data store / source of truth
		self.lookup = data['lookup']			# gives us constant time lookup to find the entries for any value -- i.e. { "age 47": [ 1, 5, 7, 9]}
		self.attributes = data['attributes']	# our attributes, stored in a list [[attr1name, [categories]], [attr2name, 'real']]
		self.continuousVariables = data['continuousVariables']
		self.categoricalVariables = data['categoricalVariables']
		self.relation = data['relation']
	
	def getData(self):
		return self.data

	# fills all missing values using the mean or mode of the class
	def fillAllMissingValues(self):
		# for each attribute
		for attr in self.attributes:
			if attr[0] + " ?" in self.lookup:	# If we have undefined variables
				print attr[0]
				if attr[1] == 'real':
					self.fillMissingContinuousValues(attr[0])
				else:
					self.fillMissingCategoricalValues(attr[0])
				print "Filled missing values for " + attr[0]

	# fills missing values for a single categorical classifier
	def fillMissingCategoricalValues(self, attrName):
		if attrName in self.categoricalVariables:
			# get and store the mode of that attribute
			mode = self.categoricalVariables[attrName].getMode()
			if (attrName + " ?") in self.lookup:
				# reverseLookup the indices of people who are missing values and iterate through them
				for entry in self.lookup[attrName + " ?"]:
					# replace their question mark with the mode
					self.data[entry][attrName] = mode
					# add to the mode in the categorical variables
					self.categoricalVariables[attrName].add(mode)
				# move indices into proper location ['attr modeName']
				for filledUserID in self.lookup[attrName + " ?"]:
					self.lookup[attrName + " " + mode]
				self.lookup.pop(attrName + " ?", 0) 		# remove from reverse lookup
			else:
				print "No missing values for " + attrName
		else:
			print "No attribute found for " + attrName

	# fills missing values for a single continuous classifier
	def fillMissingContinuousValues(self, attrName):
		if attrName in self.continuousVariables:
			# get and store the mean of that attribute
			mean = self.continuousVariables[attrName].getMean()
			if (attrName + " ?") in self.lookup:
				# reverseLookup the indices of people who are missing values and iterate through them
				for entry in self.lookup[attrName + " ?"]:
					# replace their question mark with the mean
					self.data[entry][attrName] = mean
					# add to the mean in the continuous variables
					self.continuousVariables[attrName].add(mean)
				# move indices into proper location ['attr modeName']
				for filledUserID in self.lookup[attrName + " ?"]:
					self.lookup[attrName + " " + mean]
				self.lookup.pop(attrName + " ?", 0) 		# remove from reverse lookup
			else:
				print "No missing values for " + attrName
		else:
			print "No attribute found for " + attrName
