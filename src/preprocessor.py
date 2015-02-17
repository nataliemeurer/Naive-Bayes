import utils as util
import numpy as np
import settings

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
					self.lookup[attrName + " " + mode].append(filledUserID)
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
					if attrName + " " + str(mean) in self.lookup:
						self.lookup[attrName + " " + str(mean)].append(filledUserID)
					else:
						self.lookup[attrName + " " + str(mean)] = [filledUserID]
				self.lookup.pop(attrName + " ?", 0) 		# remove from reverse lookup
			else:
				print "No missing values for " + attrName
		else:
			print "No attribute found for " + attrName

	def entropyDiscretize(self, attrName, maxNumOfBins=10):
		# declare variables
		numOfBins = 1
		splits = []
		data = []
		# create supplementary data structure to store relevant data as tuples [attr, classifier]
		for contVar in self.continuousVariables[attrName].getValues():	# for every continuous variable we have
			if len(data) == 0:
				for userId in self.lookup[attrName + " " + str(int(contVar))]:		# for every user that has that continuous variable value
					data.append([contVar, self.data[userId][settings.CLASSIFIER_NAME]])
			elif data[len(data)-1][0] != contVar:							# if we have not already allocated the users for this continuous var
				for userId in self.lookup[attrName + " " + str(int(contVar))]:		# for every user that has that continuous variable value
					data.append([contVar, self.data[userId][settings.CLASSIFIER_NAME]])
		# Use a closure scoped function to do the heavy lifting, assume items in bin(list) are dictionaries
		def findMaxEntropySplit(bin):
			maxEntropyGain = 0
			belowCount = 0
			aboveCount = 0
			for item in bin:
				if item[1] == ">50K":
					aboveCount += 1
				else:
					belowCount += 1
			if len(bin) > 0:
				initialEntropy = self.calculateEntropy(float(aboveCount) / float(len(bin))) + self.calculateEntropy(float(belowCount) / float(len(bin)))
				print initialEntropy
			countHist = numpy.matrix([0, 0], [belowCount, aboveCount])
			for


		findMaxEntropySplit(data)

	def calculateEntropy(self, prob):
		return -1 * prob * np.log2(prob)

